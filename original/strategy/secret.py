import random

def factory_secret_strategy(type: str):
    if type == "random":
        return gen_random
    elif type == "h2l2_shuffle":
        return gen_h2l2_shuffle
    elif type == "hhll":
        return gen_hhll
    else:
        raise ValueError("Unknown strategy type")

def gen_random() -> str:
    """
    0-9の数字をランダムに並べた文字列を生成する
    """
    numbers = list(range(10))
    random.shuffle(numbers)
    return ''.join(map(str, numbers{:4}))

def gen_h2l2_shuffle() -> str:
    low = list(range(5))
    high = list(range(5, 10))
    random.shuffle(low)
    random.shuffle(high)
    unique_numbers = low[:2] + high[:2]
    random.shuffle(unique_numbers)
    return ''.join(map(str, unique_numbers))

def gen_hhll() -> str:
    low = list(range(5))
    high = list(range(5, 10))
    random.shuffle(low)
    random.shuffle(high)
    unique_numbers = high[:2] + low[:2]
    return ''.join(map(str, unique_numbers))
