import random

def gen_h2l2() -> str:
    low = list(range(5))
    high = list(range(5, 10))
    random.shuffle(low)
    random.shuffle(high)
    unique_numbers = low[:2] + high[:2]
    random.shuffle(unique_numbers)
    return ''.join(map(str, unique_numbers))
