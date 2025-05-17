import math
from collections import Counter
from util import util
from util import feedback as feedback_module
import os
from concurrent.futures import ProcessPoolExecutor

def factory_estimate_strategy(type: str):
    if type == "default":
        return DefaultStrategy()
    elif type == "blandy":
        return BLandyStrategy()
    elif type == "mutual_info":
        return MutualInfoStrategy()
    else:
        raise ValueError("Unknown strategy type")

class EstimateInput:
    def __init__(self, answerList: list[str], challengeCandidates: list[str]):
        self.answerList = answerList
        self.challengeCandidates = challengeCandidates

class EstimateStrategy():
    def __init__(self):
        pass

    def setup(self):
        pass

    def teardown(self):
        pass

    def estimate(self, input: EstimateInput) -> str:
        pass

class DefaultStrategy(EstimateStrategy):
    def estimate(self, input: EstimateInput):
        return input.answerList[0]

class BLandyStrategy(EstimateStrategy):
    def _calculate_entropy(self, feedback_histogram: Counter) -> float:
        """
        フィードバックのヒストグラムからエントロピーを計算します。
        Goの提供された実装を参考にしています。
        """
        entropy = 0.0
        # フィードバックのキー（パターン文字列）でソートして計算の一貫性を保つ
        # Counter.items() は (要素, カウント) のタプルを返すので、キー item[0] でソート
        sorted_feedback_items = sorted(feedback_histogram.items(), key=lambda item: item[0])

        for fb_pattern, count in sorted_feedback_items:
            buf = 1.0
            # "4H0B" の場合、buf を 0.95 にする (solver.Digit() が 4 の場合を想定)
            if fb_pattern == "4H0B":
                buf = 0.95
            
            abs_count = abs(count) # count は常に正のはずだが、Goの実装に合わせる
            entropy += buf * abs_count * math.log(1 + abs_count)
        return entropy

    def estimate(self, input: EstimateInput) -> str:
        """
        次のターンで宣言する数字を決定します。
        宣言可能な数字ごとに、想定されるfeedbackのヒストグラムを作り、
        ヒストグラムのエントロピーが最も小さくなる宣言予定の数字を返します。

        Args:
            answerList: 相手の数字の候補のリスト。

        Returns:
            宣言予定の数字。
        """
        print("estimate: called")
        possible_declarations = input.challengeCandidates

        print("estimate: possible_declarations generated")

        if not possible_declarations:
            # 通常、create_unique_listは空のリストを返さない
            raise ValueError("宣言可能な数字のリストが生成できませんでした。")

        min_entropy = float('inf')
        best_declaration = ""
        answerList = input.answerList

        # answerListが空の場合、どの宣言候補もエントロピーは0.0となる。
        # その場合、possible_declarationsの最初の要素が選ばれる。
        if not answerList:
            # 候補がない場合、エントロピーは全ての宣言で0になる。
            # 最初の宣言可能な数字を返す。
            return possible_declarations[0]

        for declared_num_candidate in possible_declarations:
            feedback_histogram = Counter()
            
            # 現在のanswerListの各候補に対して、宣言候補とのフィードバックを計算しヒストグラムを作成
            for actual_num_candidate in answerList:
                try:
                    fb = feedback_module.calculate_hit_and_blow(declared_num_candidate, actual_num_candidate)
                    feedback_histogram[fb] += 1
                except ValueError:
                    # answerList内の不正な候補は無視（例: 重複数字、桁数違いなど）
                    # commonUtils.create_unique_list() からの declared_num_candidate は常に有効
                    continue
            
            # ヒストグラムが空の場合（answerListが全て不正な候補だったなど、稀なケース）
            if not feedback_histogram:
                current_entropy = float('inf') # この宣言は避ける
            else:
                current_entropy = self._calculate_entropy(feedback_histogram)
            
            if current_entropy < min_entropy:
                min_entropy = current_entropy
                best_declaration = declared_num_candidate
            elif current_entropy == min_entropy:
                # エントロピーが同値の場合、指示にはタイブレークのルールがないため、
                # 先に見つかったもの（possible_declarationsのイテレーション順で先のもの）を維持する。
                # もし辞書順などで選びたい場合は、ここで比較処理を追加。
                # 例: if best_declaration == "" or declared_num_candidate < best_declaration:
                #         best_declaration = declared_num_candidate
                pass
        
        print("estimate: best_declaration found")

        # best_declarationが何らかの理由で見つからなかった場合（通常は発生しないはず）
        # 例えば、全ての宣言候補でエントロピーがinfだった場合など。
        # その場合は、最初の宣言可能な数字をフォールバックとして返す。
        if not best_declaration:
            return possible_declarations[0]
                
        return best_declaration


# 並列処理のためのワーカー関数 (モジュールのトップレベルに配置)
def _worker_calculate_mi(args_tuple):
    # 引数をアンパック
    declared_num_candidate, answer_list_local_keys, current_entropy_H_X_local, \
    probabilities_local, calculate_hit_and_blow_func, \
    calculate_entropy_from_probs_func = args_tuple

    expected_conditional_entropy_H_X_given_S = 0.0
    feedback_to_posterior_info = {} #キー: fb, 値: (候補リスト, その候補リストの合計確率)

    # answer_list_local_keys は確率が0より大きい候補のキーリスト
    for actual_num_candidate in answer_list_local_keys:
        # probabilities_local から actual_num_candidate の確率を取得
        prob_actual_num_candidate = probabilities_local.get(actual_num_candidate, 0.0)
        if prob_actual_num_candidate == 0: # 確率0の候補はスキップ
            continue
        try:
            fb = calculate_hit_and_blow_func(declared_num_candidate, actual_num_candidate)
            
            current_subset_candidates, current_subset_prob_sum = feedback_to_posterior_info.get(fb, ([], 0.0))
            current_subset_candidates.append(actual_num_candidate)
            current_subset_prob_sum += prob_actual_num_candidate
            feedback_to_posterior_info[fb] = (current_subset_candidates, current_subset_prob_sum)

        except ValueError:
            continue
    
    if not feedback_to_posterior_info:
        mutual_info = -float('inf')
    else:
        # P(S) に相当する、現在の全候補の確率の合計 (正規化されていればほぼ1)
        current_total_probability_sum = sum(probabilities_local.get(cand, 0.0) for cand in answer_list_local_keys)
        if current_total_probability_sum == 0: # 通常ありえない
             return declared_num_candidate, -float('inf')

        for fb_pattern, (posterior_subset_candidates, posterior_subset_total_prob) in feedback_to_posterior_info.items():
            if posterior_subset_total_prob == 0:
                continue

            # P(R|S) = P(R) = sum_{x in posterior_subset} P(x) / sum_{all_x} P(x)
            # P(x) は現在の信念 probabilities_local[x]
            prob_feedback_p_R_given_S = posterior_subset_total_prob / current_total_probability_sum
            
            # このフィードバックが得られた後の、部分集合の正規化された確率分布
            # P(X|R,S) = P(X|S) / P(R|S) if X in R else 0
            normalized_posterior_probs = {
                cand: probabilities_local[cand] / posterior_subset_total_prob
                for cand in posterior_subset_candidates if probabilities_local.get(cand, 0.0) > 0
            }
            
            entropy_posterior_H_X_given_S_R = calculate_entropy_from_probs_func(normalized_posterior_probs)
            expected_conditional_entropy_H_X_given_S += prob_feedback_p_R_given_S * entropy_posterior_H_X_given_S_R
        
        mutual_info = current_entropy_H_X_local - expected_conditional_entropy_H_X_given_S
            
    return declared_num_candidate, mutual_info

class MutualInfoStrategy(EstimateStrategy):
    def __init__(self):
        super().__init__()
        self.probabilities: dict[str, float] = {}
        self.feedback_module = feedback_module # feedback_moduleへの参照を保持

    def setup(self):
        """
        戦略を初期化し、候補リストに基づいて確率分布を均等に設定します。
        """
        
        initial_answer_list = util.create_unique_list()
        num_candidates = len(initial_answer_list)
        if num_candidates == 0:
            self.probabilities = {}
            return
        prob_per_candidate = 1.0 / num_candidates
        self.probabilities = {candidate: prob_per_candidate for candidate in initial_answer_list}

    @staticmethod
    def _calculate_entropy_from_probabilities(probabilities: dict[str, float]) -> float:
        """
        確率分布からエントロピーを計算します。 H(X) = -sum(p_i * log2(p_i))
        """
        if not probabilities:
            return 0.0
        
        entropy = 0.0
        for prob in probabilities.values():
            if prob > 0: # log2(0) を避ける
                entropy -= prob * math.log2(prob)
        return entropy

    def _update_probabilities(self, declared_number: str, feedback: tuple[int, int]):
        """
        観測されたフィードバックに基づいて確率分布をベイズ更新します。
        P(Hypothesis_i | Data) = P(Data | Hypothesis_i) * P(Hypothesis_i) / P(Data)
        ここで Hypothesis_i は各候補、Data は観測されたフィードバック。
        P(Data | Hypothesis_i) は尤度 (likelihood)。
        P(Hypothesis_i) は事前確率 (prior probability)。
        P(Data) は正規化定数。
        """
        if not self.probabilities:
            return

        new_probabilities_unnormalized = {}
        normalization_factor = 0.0

        for candidate, prior_prob in self.probabilities.items():
            if prior_prob == 0: # 事前確率0の候補は事後確率も0
                new_probabilities_unnormalized[candidate] = 0.0
                continue
            
            try:
                # 尤度 P(Data | Hypothesis_i):
                # candidate が真の答えであると仮定したとき、declared_number に対して feedback が得られる確率。
                # この問題設定では、フィードバックは決定的であるため、尤度は1か0。
                actual_feedback = self.feedback_module.calculate_hit_and_blow(declared_number, candidate)
                likelihood = 1.0 if actual_feedback == feedback else 0.0
            except ValueError: # 不正な候補など
                likelihood = 0.0

            posterior_unnormalized = prior_prob * likelihood
            new_probabilities_unnormalized[candidate] = posterior_unnormalized
            normalization_factor += posterior_unnormalized
        
        if normalization_factor > 0:
            self.probabilities = {
                cand: unnorm_prob / normalization_factor
                for cand, unnorm_prob in new_probabilities_unnormalized.items()
            }
        else:
            # 観測されたフィードバックと矛盾しない候補が一つもなかった場合。
            # これは通常、誤ったフィードバックや、ありえない状況を示唆する。
            # 全ての候補の確率を0にするか、エラー処理を行う。
            # ここでは、全ての候補の確率を0として扱う。
            self.probabilities = {cand: 0.0 for cand in new_probabilities_unnormalized}


    def estimate(self, input_data: EstimateInput) -> str:
        # self.probabilities がこの戦略の現在の信念状態。
        # input_data.answerList は、このメソッドが呼び出される時点での外部からの情報だが、
        # ベイズ戦略では self.probabilities が主たる情報源となる。
        # setup や update_probabilities が適切に呼ばれていることを前提とする。

        active_candidates = [cand for cand, prob in self.probabilities.items() if prob > 0.0]

        if not active_candidates:
            # 確率が0より大きい候補がない場合、フォールバック。
            # challengeCandidates があればそれの先頭、なければ全候補リストから。
            fallback_declarations = input_data.challengeCandidates if input_data.challengeCandidates else util.create_unique_list()
            if not fallback_declarations:
                 raise ValueError("宣言可能な数字のリストが生成できませんでした。")
            return fallback_declarations[0]

        if len(active_candidates) == 1:
            # 候補が1つしかない場合は、それが答え。
            return active_candidates[0]

        # H(X): 現在の確率分布のエントロピー
        current_entropy_H_X = MutualInfoStrategy._calculate_entropy_from_probabilities(self.probabilities)

        # 宣言候補のリスト
        possible_declarations = input_data.challengeCandidates
        if not possible_declarations:
            # このケースは上の active_candidates が空の場合のフォールバックでもチェックされるが、念のため
            raise ValueError("宣言可能な数字のリストが生成できませんでした。")

        best_declaration = ""
        max_mutual_info = -float('inf')
        
        tasks = []
        for declared_num_candidate in possible_declarations:
            tasks.append((
                declared_num_candidate,
                active_candidates, # 確率が0より大きい候補のキーリスト
                current_entropy_H_X,
                self.probabilities, # 現在の確率分布全体
                self.feedback_module.calculate_hit_and_blow,
                MutualInfoStrategy._calculate_entropy_from_probabilities 
            ))

        run_sequentially = False
        if not tasks: # 通常、possible_declarationsがあればタスクは空にならない
            if possible_declarations: return possible_declarations[0]
            raise ValueError("処理するタスクがありません。宣言可能な数字のリストが空の可能性があります。")

        # タスク数が非常に少ない場合は並列化のオーバーヘッドが大きくなる可能性があるため逐次実行
        if len(tasks) < os.cpu_count() or len(tasks) < 4 : 
            run_sequentially = True
        
        if not run_sequentially:
            try:
                num_workers = min(os.cpu_count(), len(tasks))
                if num_workers < 1 : num_workers = 1 

                all_results = []
                with ProcessPoolExecutor(max_workers=num_workers) as executor:
                    all_results = list(executor.map(_worker_calculate_mi, tasks))
                
                for res_candidate, res_mi in all_results:
                    if res_mi > max_mutual_info:
                        max_mutual_info = res_mi
                        best_declaration = res_candidate
                    elif res_mi == max_mutual_info:
                        if not best_declaration: 
                            best_declaration = res_candidate
                        # 辞書順などのタイブレーク処理
                        elif best_declaration and res_candidate < best_declaration:
                           best_declaration = res_candidate
                
                # 全ての相互情報量が-infだった場合など、best_declarationが設定されない場合へのフォールバック
                if not best_declaration and possible_declarations:
                    best_declaration = possible_declarations[0]

            except Exception: # 例: PicklingErrorなど、並列処理中の予期せぬエラー
                # print(f"並列処理中にエラーが発生しました: {e}。逐次処理にフォールバックします。") 
                run_sequentially = True
        
        if run_sequentially:
            # 元の逐次処理ループ
            current_total_probability_sum_seq = sum(self.probabilities.get(cand, 0.0) for cand in active_candidates)
            if current_total_probability_sum_seq == 0: # 通常ありえない
                 return possible_declarations[0] if possible_declarations else util.create_unique_list()[0]

            for declared_num_candidate_seq in possible_declarations:
                expected_conditional_entropy_H_X_given_S_seq = 0.0
                feedback_to_posterior_info_seq = {} 

                for actual_num_candidate_seq in active_candidates:
                    prob_actual_num_candidate_seq = self.probabilities.get(actual_num_candidate_seq, 0.0)
                    if prob_actual_num_candidate_seq == 0:
                        continue
                    try:
                        fb_seq = self.feedback_module.calculate_hit_and_blow(declared_num_candidate_seq, actual_num_candidate_seq)
                        
                        current_subset_candidates_seq, current_subset_prob_sum_seq = feedback_to_posterior_info_seq.get(fb_seq, ([], 0.0))
                        current_subset_candidates_seq.append(actual_num_candidate_seq)
                        current_subset_prob_sum_seq += prob_actual_num_candidate_seq
                        feedback_to_posterior_info_seq[fb_seq] = (current_subset_candidates_seq, current_subset_prob_sum_seq)
                    except ValueError: 
                        continue
                
                if not feedback_to_posterior_info_seq:
                    mutual_info_seq = -float('inf')
                else:
                    for fb_pattern_seq, (posterior_subset_candidates_seq, posterior_subset_total_prob_seq) in feedback_to_posterior_info_seq.items():
                        if posterior_subset_total_prob_seq == 0:
                            continue

                        prob_feedback_p_R_given_S_seq = posterior_subset_total_prob_seq / current_total_probability_sum_seq
                        
                        normalized_posterior_probs_seq = {
                            cand: self.probabilities[cand] / posterior_subset_total_prob_seq
                            for cand in posterior_subset_candidates_seq if self.probabilities.get(cand, 0.0) > 0
                        }
                        entropy_posterior_H_X_given_S_R_seq = MutualInfoStrategy._calculate_entropy_from_probabilities(normalized_posterior_probs_seq)
                        expected_conditional_entropy_H_X_given_S_seq += prob_feedback_p_R_given_S_seq * entropy_posterior_H_X_given_S_R_seq
                    
                    mutual_info_seq = current_entropy_H_X - expected_conditional_entropy_H_X_given_S_seq

                if mutual_info_seq > max_mutual_info:
                    max_mutual_info = mutual_info_seq
                    best_declaration = declared_num_candidate_seq
                elif mutual_info_seq == max_mutual_info:
                    if not best_declaration:
                        best_declaration = declared_num_candidate_seq
                    elif best_declaration and declared_num_candidate_seq < best_declaration: 
                       best_declaration = declared_num_candidate_seq
            
            if not best_declaration and possible_declarations:
                 best_declaration = possible_declarations[0]


        if not best_declaration:
            # このフォールバックは、possible_declarationsが空でない限り、通常は到達しないはず
            if possible_declarations:
                return possible_declarations[0] 
            else:
                # フォールバック用の宣言リストも生成できない場合はエラー
                all_possible_fb = util.create_unique_list()
                if not all_possible_fb: raise ValueError("最適な宣言が見つからず、フォールバックもできませんでした。possible_declarationsが空の可能性があります。")
                return all_possible_fb[0]
            
        return best_declaration