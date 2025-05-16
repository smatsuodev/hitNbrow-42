from collections import Counter

def calculate_hit_and_blow(declared_number: str, actual_number: str) -> str:
    """
    2つの4桁の数字からヒット数とブロー数を計算し、フィードバック文字列を返します。

    Args:
        declared_number: 宣言された4桁の数字。
        actual_number: 実際の4桁の数字。

    Returns:
        フィードバック文字列 (例: "1H2B")。
    """
    hits = 0
    blows = 0
    
    if len(declared_number) != 4 or len(actual_number) != 4:
        raise ValueError("数字は4桁である必要があります。")
    if len(set(declared_number)) != 4 or len(set(actual_number)) != 4:
        raise ValueError("数字は重複しない4つの異なる数字で構成される必要があります。")

    declared_digits = list(declared_number)
    actual_digits = list(actual_number)

    # ヒットを計算
    for i in range(4):
        if declared_digits[i] == actual_digits[i]:
            hits += 1

    # ブローを計算
    for i in range(4):
        if declared_digits[i] in actual_digits and declared_digits[i] != actual_digits[i]:
            blows += 1
            
    return f"{hits}H{blows}B"

def get_feedback_patterns(declared_number: str, candidate_numbers: list[str]) -> list[tuple[str, int]]:
    """
    宣言する数字と相手の数字の候補リストから、考えうるフィードバックのパターンと
    そのパターン数を計算します。

    Args:
        declared_number: 相手に宣言する0〜9を重複なく含んだ4桁の数字。
        candidate_numbers: 現時点での相手の数字の候補のリスト。

    Returns:
        (feedbackのパターン, そのパターン数) を要素に持つリスト。
    """
    if not candidate_numbers:
        return []

    feedback_counts = Counter()

    for candidate in candidate_numbers:
        try:
            feedback = calculate_hit_and_blow(declared_number, candidate)
            feedback_counts[feedback] += 1
        except ValueError as e:
            # 不正な候補はスキップするか、エラー処理を行う
            print(f"警告: 候補 '{candidate}' は不正なためスキップされました。理由: {e}")
            continue
            
    # Counterオブジェクトを (パターン, 数) のタプルのリストに変換
    result_list = list(feedback_counts.items())
    
    # パターン文字列でソート
    # ヒット数が多い順、次にブロー数が多い順でソート
    def sort_key(item):
        h_part = item[0].split('H')[0]
        b_part = item[0].split('H')[1].split('B')[0]
        return (-int(h_part), -int(b_part))

    result_list.sort(key=sort_key)
    
    return result_list

if __name__ == '__main__':
    # テストケース
    declared = "1234"
    candidates = [
        "1234", # 4H0B
        "1243", # 2H2B
        "1324", # 2H2B
        "1235", # 3H0B
        "5678", # 0H0B
        "1567", # 1H0B
        "5167", # 0H1B
        "4321", # 0H4B
        "1345", # 1H2B
        "5134", # 0H3B
        "1256", # 2H0B
        "0123"  # 0H3B (declared="1234" の場合)
    ]
    
    print(f"宣言: {declared}")
    print(f"候補: {candidates}")
    patterns = get_feedback_patterns(declared, candidates)
    print("フィードバックパターン:")
    for pattern, count in patterns:
        print(f"- {pattern}: {count}回")

    print("\n別のテストケース:")
    declared_2 = "0739"
    candidates_2 = [
        "0739", # 4H0B
        "0793", # 2H2B
        "1245", # 0H0B
        "0123", # 1H1B (0,3)
        "7039", # 2H2B
        "3907", # 0H4B
        "0731", # 3H0B
    ]
    print(f"宣言: {declared_2}")
    print(f"候補: {candidates_2}")
    patterns_2 = get_feedback_patterns(declared_2, candidates_2)
    print("フィードバックパターン:")
    for pattern, count in patterns_2:
        print(f"- {pattern}: {count}回")

    print("\n不正な候補を含むテストケース:")
    declared_3 = "1234"
    candidates_3 = [
        "1234",
        "1123", # 不正 (重複あり)
        "123",  # 不正 (3桁)
        "5678"
    ]
    print(f"宣言: {declared_3}")
    print(f"候補: {candidates_3}")
    patterns_3 = get_feedback_patterns(declared_3, candidates_3)
    print("フィードバックパターン:")
    for pattern, count in patterns_3:
        print(f"- {pattern}: {count}回")