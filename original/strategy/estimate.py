import math
from collections import Counter
import sys
from util import util
from util import feedback as feedback_module
import os
from concurrent.futures import ProcessPoolExecutor
import functools # For memoization
import time # 時間計測のため

def factory_estimate_strategy(type: str):
    if type == "default":
        return DefaultStrategy()
    elif type == "blandy":
        return BLandyStrategy()
    elif type == "blandy-dist":
        return BLandyDistStrategy()
    elif type == "mutual_info":
        return MutualInfoStrategy()
    elif type == "minimax":
        return MiniMaxStrategy()
    elif type == "blandy-minimax":
        return BLandyMiniMaxStrategy()
    else:
        raise ValueError("Unknown strategy type")

class EstimateInput:
    def __init__(self, answer_list: list[str], challenge_candidates: list[str], answer_list_oppo: list[str]):
        self.answer_list = answer_list
        self.challenge_candidates = challenge_candidates
        self.answer_list_oppo = answer_list_oppo

class EstimateStrategy():
    def __init__(self):
        pass

    def setup(self):
        pass

    def teardown(self):
        pass

    def estimate(self, input: EstimateInput) -> str:
        pass

    def on_feedback(self, declared_number: str, feedback: str):
        """
        フィードバックを受け取ったときの処理。
        デフォルトでは何もしない。
        """
        pass

class DefaultStrategy(EstimateStrategy):
    def estimate(self, input: EstimateInput):
        return input.answer_list[0]

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
        possible_declarations = input.challenge_candidates

        print("estimate: possible_declarations generated")

        if not possible_declarations:
            # 通常、create_unique_listは空のリストを返さない
            raise ValueError("宣言可能な数字のリストが生成できませんでした。")

        min_entropy = float('inf')
        best_declaration = ""
        answerList = input.answer_list

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

class BLandyDistStrategy(EstimateStrategy):
    def _calculate_entropy(self, feedback_histogram: Counter) -> float:
        """
        フィードバックのヒストグラムからエントロピーを計算します。
        Goの提供された実装を参考にしています。
        """
        entropy = 0.0
        # フィードバックのキー（パターン文字列）でソートして計算の一貫性を保つ
        # Counter.items() は (要素, カウント) のタプルを返すので、キー item[0] でソート
        sorted_feedback_items = sorted(feedback_histogram.items(), key=lambda item: item[0])
        average = sum(feedback_histogram.values()) / len(feedback_histogram)
        deviation = math.sqrt(sum(map(lambda x: (x-average)**2, feedback_histogram.values())))

        for fb_pattern, count in sorted_feedback_items:
            buf = 1.0
            # "4H0B" の場合、buf を 0.95 にする (solver.Digit() が 4 の場合を想定)
            if fb_pattern == "4H0B":
                buf = 0.95
            
            abs_count = abs(count) # count は常に正のはずだが、Goの実装に合わせる
            entropy += buf * abs_count * math.log(1 + abs_count)
        return entropy * deviation

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
        possible_declarations = input.challenge_candidates

        print("estimate: possible_declarations generated")

        if not possible_declarations:
            # 通常、create_unique_listは空のリストを返さない
            raise ValueError("宣言可能な数字のリストが生成できませんでした。")

        min_entropy = float('inf')
        best_declaration = ""
        answerList = input.answer_list

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

    def on_feedback(self, declared_number: str, feedback: str):
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
        # if len(input_data.challengeCandidates) == 5040:
        #     # どうせこれを返すのでキャッシュする
        #     return "1245"

        # self.probabilities がこの戦略の現在の信念状態。
        # input_data.answerList は、このメソッドが呼び出される時点での外部からの情報だが、
        # ベイズ戦略では self.probabilities が主たる情報源となる。
        # setup や update_probabilities が適切に呼ばれていることを前提とする。

        active_candidates = [cand for cand, prob in self.probabilities.items() if prob > 0.0]

        if not active_candidates:
            # 確率が0より大きい候補がない場合、フォールバック。
            # challengeCandidates があればそれの先頭、なければ全候補リストから。
            fallback_declarations = input_data.challenge_candidates if input_data.challenge_candidates else util.create_unique_list()
            if not fallback_declarations:
                 raise ValueError("宣言可能な数字のリストが生成できませんでした。")
            return fallback_declarations[0]

        if len(active_candidates) == 1:
            # 候補が1つしかない場合は、それが答え。
            return active_candidates[0]

        # H(X): 現在の確率分布のエントロピー
        current_entropy_H_X = MutualInfoStrategy._calculate_entropy_from_probabilities(self.probabilities)

        # 宣言候補のリスト
        possible_declarations = input_data.challenge_candidates
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

class MiniMaxStrategy(EstimateStrategy):
    def __init__(self):
        super().__init__()
        self.TIME_LIMIT_SECONDS = 7.8  # 8秒の制限に対し少しマージン
        self.memo = {} # メモ化用辞書: (my_cand_tuple, oppo_cand_tuple, turn, is_maximizing, depth, maximizer_options_tuple, minimizer_options_tuple) -> eval
        self.maximizer_declarer_options_static = [] # estimate呼び出し時に設定
        self.minimizer_declarer_options_static = [] # estimate呼び出し時に設定


    def _evaluate_state_terminal(self, am_i_winner: bool, turn: int) -> float:
        """
        決着がついた局面の評価値を計算します。
        Args:
            am_i_winner: 自分が勝者かどうか。
            turn: 決着がついた手番（0から始まる）。
        Returns:
            評価値。
        """
        # 決着がついた場合: 1/(ターン数 + 1) * 1000
        # ターン数は、その決着がついた行動が行われた「手番」を指す。
        # 例えば、1手目（turn=0）で決着なら、(0+1)で除算。
        score = (1.0 / (turn + 1.0)) * 1000.0
        return score if am_i_winner else -score

    def _evaluate_intermediate_state(self, my_candidates: list[str], opponent_candidates: list[str], turn: int) -> float:
        """
        途中の局面の評価値を計算します。
        Args:
            my_candidates: 自分の残りの候補リスト。
            opponent_candidates: 相手の残りの候補リスト。
            turn: 現在の手番（0から始まる）。
        Returns:
            評価値。スコアが高いほど自分に有利。
        """
        # ===================== ここから評価関数 (途中の局面) =====================
        # 設計方針:
        # - 相手の候補が少ないほど、自分にとって有利（相手を追い詰めている）。
        # - 自分の候補が少ないほど、相手にとって有利（自分が追い詰められている）。
        # - 単純な差分や比率で表現。
        
        if not my_candidates: # 自分の候補がない -> 自分が矛盾/負け
            return -10000.0 # 十分に低い値
        if not opponent_candidates: # 相手の候補がない -> 相手が矛盾/勝ち
            return 10000.0  # 十分に高い値

        # 相手の候補数の逆数を自分の有利度、自分の候補数の逆数を相手の有利度（自分の不利度）とする。
        # スケールを調整するために適当な係数をかけることも可能。
        my_advantage = 100.0 / (len(opponent_candidates) + 1e-6)  # ゼロ除算防止
        opponent_advantage = 100.0 / (len(my_candidates) + 1e-6)
        
        score = my_advantage - opponent_advantage
        # ===================== ここまで評価関数 (途中の局面) =====================
        return score

    def _update_candidates_list(self, candidates: list[str], declared_number: str, feedback: str) -> list[str]:
        """
        与えられたフィードバックに基づいて候補リストを更新します。
        """
        return [
            cand for cand in candidates
            if feedback_module.calculate_hit_and_blow(declared_number, cand) == feedback
        ]

    def _minimax_recursive(self, 
                           my_candidates: list[str], 
                           opponent_candidates: list[str],
                           depth: int, 
                           turn: int, 
                           is_maximizing_player: bool,
                           alpha: float, 
                           beta: float, 
                           start_time: float,
                           current_maximizer_declarer_options: tuple[str, ...], # 変更: タプルで渡す
                           current_minimizer_declarer_options: tuple[str, ...]): # 変更: タプルで渡す

        state_key = (
            tuple(sorted(my_candidates)), 
            tuple(sorted(opponent_candidates)), 
            turn, 
            is_maximizing_player, 
            depth,
            current_maximizer_declarer_options, # メモ化キーに含める
            current_minimizer_declarer_options  # メモ化キーに含める
        )
        if state_key in self.memo:
            return self.memo[state_key]

        if time.time() - start_time > self.TIME_LIMIT_SECONDS:
            raise TimeoutError("Time limit exceeded in _minimax_recursive")

        # ベースケース: 深さ0、またはどちらかの候補がなくなったら中間評価
        if depth == 0 or not my_candidates or not opponent_candidates:
            val = self._evaluate_intermediate_state(my_candidates, opponent_candidates, turn)
            self.memo[state_key] = val
            return val

        if is_maximizing_player: # 自分の手番 (Max player)
            max_eval = -float('inf')
            # 自分の可能な宣言手
            for my_call in current_maximizer_declarer_options:
                # この宣言 `my_call` に対する評価値を計算 (相手の真の答えの全可能性を考慮)
                evals_for_this_my_call_branches = []
                
                for oppo_real_answer in opponent_candidates:
                    feedback_to_me = feedback_module.calculate_hit_and_blow(my_call, oppo_real_answer)

                    if feedback_to_me == "4H0B": # 自分が正解を当てた
                        eval_of_branch = self._evaluate_state_terminal(True, turn) # 現在のターンで決着
                    else:
                        updated_my_candidates = self._update_candidates_list(my_candidates, my_call, feedback_to_me)
                        if not updated_my_candidates: # 矛盾 (このoppo_real_answerはありえない)
                            continue 
                        eval_of_branch = self._minimax_recursive(
                            updated_my_candidates, opponent_candidates, # opponent_candidates はまだ変わらない
                            depth - 1, turn + 1, False, # 次は相手(Min player)の手番
                            alpha, beta, start_time,
                            current_maximizer_declarer_options, 
                            current_minimizer_declarer_options
                        )
                    evals_for_this_my_call_branches.append(eval_of_branch)
                
                if not evals_for_this_my_call_branches:
                    # このmy_callは、相手の全ての候補と矛盾したか、opponent_candidatesが空だった。
                    # opponent_candidatesが空の場合はベースケースで処理される。
                    # よって、updated_my_candidatesが常に空になった場合。これは自殺手。
                    current_call_value = -float('inf') 
                else:
                    # 相手は自分にとって最悪の状況を選ぶ (Min playerなので最小値)
                    current_call_value = min(evals_for_this_my_call_branches)
                
                max_eval = max(max_eval, current_call_value)
                alpha = max(alpha, max_eval)
                if beta <= alpha:
                    break # Beta cut-off
            
            self.memo[state_key] = max_eval
            return max_eval

        else: # 相手の手番 (Min player)
            min_eval = float('inf')
            # 相手の可能な宣言手
            for oppo_call in current_minimizer_declarer_options:
                evals_for_this_oppo_call_branches = []

                for my_real_answer in my_candidates:
                    feedback_to_oppo = feedback_module.calculate_hit_and_blow(oppo_call, my_real_answer)

                    if feedback_to_oppo == "4H0B": # 相手が正解を当てた
                        eval_of_branch = self._evaluate_state_terminal(False, turn) # 現在のターンで決着
                    else:
                        updated_opponent_candidates = self._update_candidates_list(opponent_candidates, oppo_call, feedback_to_oppo)
                        if not updated_opponent_candidates: # 矛盾 (このmy_real_answerはありえない)
                            continue
                        eval_of_branch = self._minimax_recursive(
                            my_candidates, updated_opponent_candidates, # my_candidates はまだ変わらない
                            depth - 1, turn + 1, True, # 次は自分(Max player)の手番
                            alpha, beta, start_time,
                            current_maximizer_declarer_options,
                            current_minimizer_declarer_options
                        )
                    evals_for_this_oppo_call_branches.append(eval_of_branch)

                if not evals_for_this_oppo_call_branches:
                    # このoppo_callは、自分の全ての候補と矛盾した。相手の自殺手。
                    current_call_value = float('inf')
                else:
                    # 自分は相手にとって最悪の状況を選ぶ (Max playerなので最大値)
                    # (相手の視点では、相手にとって最良の自分の手を選ぶ)
                    current_call_value = max(evals_for_this_oppo_call_branches)

                min_eval = min(min_eval, current_call_value)
                beta = min(beta, min_eval)
                if beta <= alpha:
                    break # Alpha cut-off
            
            self.memo[state_key] = min_eval
            return min_eval

    def estimate(self, input_data: EstimateInput) -> str:
        start_time = time.time()
        self.memo.clear() # 新しい探索ごとにメモをクリア

        # 宣言候補リストをタプルに変換して不変にする（メモ化キーのため）
        # これらは _minimax_recursive に渡される
        maximizer_options_tuple = tuple(sorted(input_data.challenge_candidates))
        minimizer_options_tuple = tuple(sorted(util.create_unique_list()))


        if not input_data.challenge_candidates:
            return util.create_unique_list()[0] if util.create_unique_list() else "1234" # フォールバック
        
        # 初期状態でどちらかの候補リストが空の場合の処理
        if not input_data.answer_list or not input_data.answer_list_oppo:
            # 評価関数で処理されるが、探索に入る前に単純な手を返すこともできる
            # ここでは探索に任せるが、もし問題があればここで早期リターンを追加
            pass


        best_move_overall = input_data.challenge_candidates[0] # デフォルトの最善手
        best_eval_overall = -float('inf')
        
        current_turn_for_estimate = 0 # estimateは最初のターン(turn=0)の行動を決定

        # IDDFS (Iterative Deepening Depth-First Search)
        # 現実的な最大深さ。時間制限があるので、ここまで到達しないことが多い。
        # Hit&Blowのゲームの長さは通常10ターン以内なので、深さもそれに応じて。
        # 1手で2ply進む (自分と相手) と考えると、深さ5で10手先。
        max_depth_limit = 6 
        for depth in range(1, max_depth_limit + 1):
            current_best_move_for_this_depth = None
            current_max_eval_for_this_depth = -float('inf')
            
            if time.time() - start_time > self.TIME_LIMIT_SECONDS:
                print(f"Time limit reached before starting depth {depth}. Using best move from prior depths: {best_move_overall}", file=sys.stderr)
                break

            try:
                # 自分の最初の宣言候補をループ
                for my_call_candidate in maximizer_options_tuple:
                    if time.time() - start_time > self.TIME_LIMIT_SECONDS:
                        print(f"Time limit reached during move selection (depth {depth}). Using best move found so far for this depth.", file=sys.stderr)
                        raise TimeoutError # この深さの探索を中断

                    # この宣言 `my_call_candidate` に対する評価値を計算
                    evals_for_this_my_call_branches = []
                    if not input_data.answer_list_oppo: # 相手の候補が既にない
                        # このケースは通常、_evaluate_intermediate_stateで高評価になる
                        # ここでは、相手の候補がないのでループできない。
                        # このコール自体の評価は、この盤面評価になる。
                        evals_for_this_my_call_branches.append(self._evaluate_intermediate_state(input_data.answer_list, [], current_turn_for_estimate))

                    for oppo_real_answer in input_data.answer_list_oppo:
                        feedback_to_me = feedback_module.calculate_hit_and_blow(my_call_candidate, oppo_real_answer)

                        if feedback_to_me == "4H0B": # 自分が初手で当てた！
                            eval_of_branch = self._evaluate_state_terminal(True, current_turn_for_estimate)
                        else:
                            updated_my_candidates = self._update_candidates_list(input_data.answer_list, my_call_candidate, feedback_to_me)
                            if not updated_my_candidates: # このoppo_real_answerと矛盾
                                continue
                            
                            # 次は相手の手番 (Minimizing player)
                            # 初手なので、alphaは-inf, betaは+infで開始
                            eval_of_branch = self._minimax_recursive(
                                updated_my_candidates, input_data.answer_list_oppo,
                                depth - 1, # 再帰の深さ (現在の深さから1減らす)
                                current_turn_for_estimate + 1, 
                                False, # is_maximizing_player = False (相手の手番)
                                -float('inf'), float('inf'), # Alpha, Beta
                                start_time,
                                maximizer_options_tuple,
                                minimizer_options_tuple
                            )
                        evals_for_this_my_call_branches.append(eval_of_branch)
                    
                    if not evals_for_this_my_call_branches:
                        # このmy_call_candidateは、相手の全ての候補と矛盾した。自殺手。
                        current_call_value = -float('inf')
                    else:
                        # 相手は自分にとって最悪の状況を選ぶ (Min playerなので最小値)
                        current_call_value = min(evals_for_this_my_call_branches)

                    if current_call_value > current_max_eval_for_this_depth:
                        current_max_eval_for_this_depth = current_call_value
                        current_best_move_for_this_depth = my_call_candidate
                
                if current_best_move_for_this_depth is not None:
                    best_move_overall = current_best_move_for_this_depth
                    best_eval_overall = current_max_eval_for_this_depth
                    print(f"Depth {depth}: Best move {best_move_overall} with eval {best_eval_overall:.2f} (Time: {time.time()-start_time:.2f}s)", file=sys.stderr)
                else:
                    # この深さで有効な手が見つからなかった場合 (通常は起こりにくい)
                    print(f"Depth {depth}: No valid move found. (Time: {time.time()-start_time:.2f}s)", file=sys.stderr)
                    # この深さで手が見つからなければ、それ以上深くしても無駄なので抜ける
                    if depth > 1: # 最初の深さでなければ、前の深さの結果を使う
                         print(f"No move found at depth {depth}, using best from prior: {best_move_overall}", file=sys.stderr)
                    break 

            except TimeoutError:
                print(f"Timeout at depth {depth}. Using best move from this depth if any, or prior: {best_move_overall}", file=sys.stderr)
                if current_best_move_for_this_depth is not None : # この深さで途中まででも手が見つかっていれば更新
                    best_move_overall = current_best_move_for_this_depth
                    best_eval_overall = current_max_eval_for_this_depth
                break # IDDFSループを終了
            except Exception as e:
                print(f"Error during MiniMax estimate at depth {depth}: {e}", file=sys.stderr)
                import traceback
                traceback.print_exc(file=sys.stderr)
                break # エラー発生時も探索終了

        print(f"MiniMax final best move: {best_move_overall}, Eval: {best_eval_overall:.2f}, Total time: {time.time()-start_time:.2f}s", file=sys.stderr)
        
        # 万が一 best_move_overall が None のままの場合のフォールバック
        if best_move_overall is None:
            if input_data.challenge_candidates:
                return input_data.challenge_candidates[0]
            elif util.create_unique_list():
                return util.create_unique_list()[0]
            else:
                return "1234" # 最終フォールバック
                
        return best_move_overall

class BLandyMiniMaxStrategy(EstimateStrategy):
    def __init__(self):
        super().__init__()
        self.blandy = factory_estimate_strategy("blandy")
        self.minimax = factory_estimate_strategy("minimax")
    
    def setup(self):
        self.blandy.setup()
        self.minimax.setup()

    def teardown(self):
        self.blandy.teardown()
        self.minimax.teardown()

    def estimate(self, input_data: EstimateInput) -> str:
        if len(input_data.answer_list) <= 25:
            # print(f"use minimax: {len(input_data.answer_list)}", file=sys.stderr)
            return self.minimax.estimate(input_data)
        
        return self.blandy.estimate(input_data)