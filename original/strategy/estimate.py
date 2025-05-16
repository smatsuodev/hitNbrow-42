import math
from collections import Counter
from util import commonUtils
from util import feedback as feedback_module

class EstimateInput:
    def __init__(self, answerList: list[str]):
        self.answerList = answerList

class EstimateStrategy():
    def __init__(self):
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
        # possible_declarations = commonUtils.create_unique_list() # 宣言可能な全パターンを走査する場合はこっち
        possible_declarations = input.answerList # 4H0B狙いの場合はこっち

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

