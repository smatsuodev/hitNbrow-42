from collections import Counter
import math

def _calculate_entropy(self, hist: Counter) -> float:
    """
    フィードバックのヒストグラムからエントロピーを計算します。
    Goの提供された実装を参考にしています。
    """
    entropy = 0.0
    # フィードバックのキー（パターン文字列）でソートして計算の一貫性を保つ
    # Counter.items() は (要素, カウント) のタプルを返すので、キー item[0] でソート
    sorted_items = sorted(hist.items(), key=lambda item: item[0])

    for _, count in sorted_items:
        buf = 1.0
        
        abs_count = abs(count) # count は常に正のはずだが、Goの実装に合わせる
        entropy += buf * abs_count * math.log(1 + abs_count)
    return entropy

def _do_target(self, answer_list: list[str]) -> str:
    used_numbers = set()
    for answer in answer_list:
        for digit in answer:
            used_numbers.add(digit)

    used_numbers = list(used_numbers)
    min_entropy = float("inf")
    best_target = ""

    if not answer_list:
        return used_numbers[0]

    for target in used_numbers:
        hist = Counter()

        for answer in answer_list:
            index = answer.find(target)
            hist[index] += 1

        
        if not hist:
            current_entropy = float('inf') # この宣言は避ける
        else:
            current_entropy = self._calculate_entropy(hist)

        if current_entropy < min_entropy:
            min_entropy = current_entropy
            best_target = target
        elif current_entropy == min_entropy:
            # エントロピーが同値の場合、指示にはタイブレークのルールがないため、
            # 先に見つかったもの（possible_declarationsのイテレーション順で先のもの）を維持する。
            # もし辞書順などで選びたい場合は、ここで比較処理を追加。
            # 例: if best_declaration == "" or declared_num_candidate < best_declaration:
            #         best_declaration = declared_num_candidate
            pass

    return best_target
