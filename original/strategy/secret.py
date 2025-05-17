import random

def factory_secret_strategy(type: str):
    if type == "h2l2":
        return gen_h2l2
    elif type == "random":
        return gen_random
    else:
        raise ValueError("Unknown strategy type")

def gen_random() -> str:
    """
    0-9の数字をランダムに並べた文字列を生成する
    """
    numbers = list(range(10))
    random.shuffle(numbers)
    return ''.join(map(str, numbers))

def gen_h2l2() -> str:
    low = list(range(5))
    high = list(range(5, 10))
    random.shuffle(low)
    random.shuffle(high)
    unique_numbers = low[:2] + high[:2]
    random.shuffle(unique_numbers)
    return ''.join(map(str, unique_numbers))
