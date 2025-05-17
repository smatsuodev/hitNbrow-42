def calculate_hit_blow(secret: str, challenge: str) -> tuple[int, int]:
    """
    secretとchallengeのhitとblowを計算してタプルで返す
    """

    # 想定として、secretとchallengeは同じ桁数であることを前提とします。
    # もし桁数が異なる場合の処理が必要であれば、ここに追加してください。
    if len(secret) != len(challenge):
        # 例: 異なる桁数の場合は (0, 0) を返すか、エラーを発生させる
        # raise ValueError("SecretとChallengeの桁数が異なります。")
        return 0, 0 # ここでは仮に0,0を返します

    hit = 0
    blow = 0

    # ヒットの計算
    for i in range(len(challenge)):
        if challenge[i] == secret[i]:
            hit += 1
            continue

        if challenge[i] in secret:
            blow += 1

    return hit, blow

def add_change(old: list[str], pos: int, highlow: str) -> list[str]:
    """
    oldのpos番目をhighかlowに変更して、答えの候補を返す
    """
    high = list(range(5, 10))
    low = list(range(0, 5))

    new_answers = set()

    for ans in old:
        src = high if highlow == "high" else low

        for n in src:
            new_ans = ans[:pos] + str(n) + ans[pos + 1:]
            new_answers.add(new_ans)

    return list(new_answers)

def add_shuffle(old: list[str]) -> list[str]:
    """
    oldAnswersを並び替えた場合の答えの候補を返す
    """
    from itertools import permutations

    new_answers = set()
    for item in old:
        # 文字列の各文字のすべての順列を生成
        for p in permutations(item):
            new_answers.add("".join(p))
    return list(new_answers)

def delete_bad_answer(hit: int, blow: int, number: str, old: list[str]) -> list[str]:
    """
    宣言したnumberとそれに対するhit, blowの結果を元に、矛盾する候補をoldから削除する
    """
    new_answers = []
    for ans_candidate in old:
        current_hit, current_blow = calculate_hit_blow(ans_candidate, number)
                
        if current_hit == hit and current_blow == blow:
            new_answers.append(ans_candidate)
            
    return new_answers

def delete_bad_answer_high_low(high: int, low: int, old: list[str]) -> list[str]:
    """
    判明したhigh, lowの結果を元に、矛盾する候補をoldから削除する
    """
    new_answers = []
    for ans_candidate in old:
        current_high = 0
        current_low = 0
        for digit_char in ans_candidate:
            digit = int(digit_char)
            if 0 <= digit <= 4:
                current_low += 1
            elif 5 <= digit <= 9:
                current_high += 1
        
        if current_high == high and current_low == low:
            new_answers.append(ans_candidate)
            
    return new_answers

def delete_bad_answer_target(target: str, pos: int, old: list[str]) -> list[str]:
    """
    posが桁数の範囲内の場合は、oldのpos番目がtargetと一致するものを返す
    posが桁数の範囲外の場合は、targetを含まないものを返す
    """
    new_answers = []
    for ans_candidate in old:
        if pos < len(ans_candidate) and pos >= 0:
            if ans_candidate[pos] == target:
                new_answers.append(ans_candidate)
        else:
            if target not in ans_candidate:
                new_answers.append(ans_candidate)

    return new_answers

def create_unique_list() -> list[str]:
    """
    0-9を重複なく並べた4桁の文字列を全パターン生成する
    """

    # 0-9の数字をリストに格納
    numbers = list(range(10))

    # 4桁の全パターンを生成
    from itertools import permutations
    all_combinations = permutations(numbers, 4)

    # 各組み合わせを文字列に変換してリストに格納
    unique_list = [''.join(map(str, combination)) for combination in all_combinations]

    return unique_list
