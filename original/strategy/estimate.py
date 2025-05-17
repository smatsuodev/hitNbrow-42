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
    declared_num_candidate, answer_list_local, current_entropy_H_X_local, \
    total_answers_in_list_local, calculate_hit_and_blow_func, \
    static_calculate_entropy_func = args_tuple

    expected_conditional_entropy_H_X_given_S = 0.0
    feedback_to_posterior_subset = {}

    for actual_num_candidate in answer_list_local:
        try:
            fb = calculate_hit_and_blow_func(declared_num_candidate, actual_num_candidate)
            feedback_to_posterior_subset.setdefault(fb, []).append(actual_num_candidate)
        except ValueError:
            continue
    
    if not feedback_to_posterior_subset:
        mutual_info = -float('inf')
    else:
        for fb_pattern, posterior_subset in feedback_to_posterior_subset.items():
            prob_feedback_p_R_given_S = len(posterior_subset) / total_answers_in_list_local
            entropy_posterior_H_X_given_S_R = static_calculate_entropy_func(posterior_subset)
            expected_conditional_entropy_H_X_given_S += prob_feedback_p_R_given_S * entropy_posterior_H_X_given_S_R
        
        mutual_info = current_entropy_H_X_local - expected_conditional_entropy_H_X_given_S
            
    return declared_num_candidate, mutual_info

class MutualInfoStrategy(EstimateStrategy):
    @staticmethod # 並列処理で使いやすくする
    def _calculate_entropy_from_list(current_answer_list: list[str]) -> float:
        """
        候補リストからエントロピーを計算します。
        リスト内の各項目は等確率であると仮定します。
        H(X) = log2(N) ここで N はアイテム数。
        """
        n = len(current_answer_list)
        if n <= 1:  # log2(1)=0. n=0 の場合、情報量は0。
            return 0.0
        return math.log2(n)

    def estimate(self, input_data: EstimateInput) -> str: # Renamed input to input_data to avoid conflict with builtin
        answerList = input_data.answerList
        
        if not answerList:
            # 候補リストが空の場合、宣言可能な最初の数字をフォールバックとして返す
            all_possible_declarations_fb = util.create_unique_list()
            if not all_possible_declarations_fb:
                 raise ValueError("宣言可能な数字のリストが生成できませんでした。")
            return all_possible_declarations_fb[0]

        if len(answerList) == 1:
            # 候補が1つしかない場合は、それが答え
            return answerList[0]

        # H(X): 現在の候補リストのエントロピー
        current_entropy_H_X = MutualInfoStrategy._calculate_entropy_from_list(answerList) # staticmethodとして呼び出し

        # 宣言候補のリスト
        possible_declarations = input_data.challengeCandidates
        if not possible_declarations:
            # このケースは上の answerList が空の場合のフォールバックでもチェックされるが、念のため
            raise ValueError("宣言可能な数字のリストが生成できませんでした。")

        best_declaration = ""
        max_mutual_info = -float('inf')
        
        total_answers_in_list = len(answerList)

        tasks = []
        for declared_num_candidate in possible_declarations:
            tasks.append((
                declared_num_candidate,
                answerList, 
                current_entropy_H_X,
                total_answers_in_list,
                feedback_module.calculate_hit_and_blow, # 関数自体を渡す
                MutualInfoStrategy._calculate_entropy_from_list # staticmethodを渡す
            ))

        run_sequentially = False
        if not tasks:
            if possible_declarations: return possible_declarations[0]
            raise ValueError("処理するタスクがありません。宣言可能な数字のリストが空の可能性があります。")

        # タスク数が非常に少ない場合は並列化のオーバーヘッドが大きくなる可能性があるため逐次実行
        # この閾値は環境や問題のサイズによって調整が必要
        if len(tasks) < os.cpu_count() or len(tasks) < 4 : # 例: CPUコア数未満または4未満なら逐次
            run_sequentially = True
        
        if not run_sequentially:
            try:
                num_workers = min(os.cpu_count(), len(tasks))
                if num_workers < 1 : num_workers = 1 # 少なくとも1ワーカー

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
                        # 必要であれば辞書順などのタイブレーク処理を追加
                        # elif best_declaration and res_candidate < best_declaration:
                        #    best_declaration = res_candidate
                
                # 全ての相互情報量が-infだった場合など、best_declarationが設定されない場合へのフォールバック
                if not best_declaration and possible_declarations:
                    best_declaration = possible_declarations[0]

            except Exception: # 例: PicklingErrorなど、並列処理中の予期せぬエラー
                # print(f"並列処理中にエラーが発生しました: {e}。逐次処理にフォールバックします。") # 必要に応じてログ出力
                run_sequentially = True
        
        if run_sequentially:
            # 元の逐次処理ループ
            for declared_num_candidate_seq in possible_declarations:
                expected_conditional_entropy_H_X_given_S_seq = 0.0
                feedback_to_posterior_subset_seq = {} 

                for actual_num_candidate_seq in answerList:
                    try:
                        fb_seq = feedback_module.calculate_hit_and_blow(declared_num_candidate_seq, actual_num_candidate_seq)
                        feedback_to_posterior_subset_seq.setdefault(fb_seq, []).append(actual_num_candidate_seq)
                    except ValueError: 
                        continue
                
                if not feedback_to_posterior_subset_seq:
                    mutual_info_seq = -float('inf')
                else:
                    for fb_pattern_seq, posterior_subset_seq in feedback_to_posterior_subset_seq.items():
                        prob_feedback_p_R_given_S_seq = len(posterior_subset_seq) / total_answers_in_list
                        entropy_posterior_H_X_given_S_R_seq = MutualInfoStrategy._calculate_entropy_from_list(posterior_subset_seq)
                        expected_conditional_entropy_H_X_given_S_seq += prob_feedback_p_R_given_S_seq * entropy_posterior_H_X_given_S_R_seq
                    
                    mutual_info_seq = current_entropy_H_X - expected_conditional_entropy_H_X_given_S_seq

                if mutual_info_seq > max_mutual_info:
                    max_mutual_info = mutual_info_seq
                    best_declaration = declared_num_candidate_seq
                elif mutual_info_seq == max_mutual_info:
                    if not best_declaration:
                        best_declaration = declared_num_candidate_seq
                    # elif best_declaration and declared_num_candidate_seq < best_declaration: # Optional tie-break
                    #    best_declaration = declared_num_candidate_seq
            
            if not best_declaration and possible_declarations:
                 best_declaration = possible_declarations[0]


        if not best_declaration:
            # このフォールバックは、possible_declarationsが空でない限り、通常は到達しないはず
            if possible_declarations:
                return possible_declarations[0] 
            else:
                raise ValueError("最適な宣言が見つからず、フォールバックもできませんでした。possible_declarationsが空の可能性があります。")
            
        return best_declaration