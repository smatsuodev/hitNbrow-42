
from functools import lru_cache
import random


@lru_cache(maxsize=None)
def create_unique_list():
    ret = []
    for i in range(10):
        for j in range(10):
            if i == j:
                continue
            for k in range(10):
                if i == k or j == k:
                    continue
                for l in range(10):
                    if i == l or j == l or k == l:
                        continue
                    str_val = f"{i}{j}{k}{l}"
                    ret.append(str_val)
    return ret

def collect_unique_digits_suf(numbers_list):
    
    ret = []
    for i in numbers_list:
        for j in numbers_list:
            if i == j:
                continue
            for k in numbers_list:
                if i == k or j == k:
                    continue
                for l in numbers_list:
                    if i == l or j == l or k == l:
                        continue
                    str_val = f"{i}{j}{k}{l}"
                    ret.append(str_val)
    return ret

def addSuffle(answer_list):
    unique_list = set()
    for number_str in answer_list:
        if number_str in unique_list:
            continue
        for i in number_str:
            for j in number_str:
                if i == j:
                    continue
                for k in number_str:
                    if i == k or j == k:
                        continue
                    for l in number_str:
                        if i == l or j == l or k == l:
                            continue
                        str_val = f"{i}{j}{k}{l}"
                        unique_list.add(str_val)
    return list(unique_list)

def add_change(answer_list, position, high_low):
    unique_temp_answer_list = set()
    all_low_digits = set(['0', '1', '2', '3', '4'])

    all_high_digits = set(['5', '6', '7', '8', '9'])
    for number_str in answer_list:
        if int(number_str[position]) >= 5 and high_low == "low":
             continue
        if int(number_str[position]) < 5 and high_low == "high":
             continue
        digit_list = set(number_str)
        unused_digits = set()
        if (high_low == "high"):
            unused_digits = all_high_digits - digit_list
        else :
            unused_digits = all_low_digits - digit_list
        for b in unused_digits:
            new_string = number_str[:position] + b + number_str[position+1:]
            unique_temp_answer_list.add(new_string)
    return list(unique_temp_answer_list)

def do_change(answer_list_oppo, secret):
    all_digits = set(['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'])
    digit_count = {digit: 0 for digit in secret}
    secret_list = set(secret);
    unused_digits_set = all_digits - secret_list
    unused_digits = list(unused_digits_set)
    for number_str in answer_list_oppo:
        for digit in number_str:
            if digit in digit_count:
                digit_count[digit] += 1
    most_frequent_digit = max(digit_count, key=digit_count.get)
    is_high = int(digit) >= 5;
    highlow = ""
    if is_high:
        highlow = "high"
    else:
        highlow = "low"
    for i in range(len(secret)):
        if (secret[i] == most_frequent_digit):
            new_secret = secret[:i] + get_change_number(unused_digits, most_frequent_digit) + secret[i+1:]
            return [new_secret, i, highlow]


def get_change_number(unused_digits, digit):
    if int(digit) >= 5:
        return random.choice([x for x in unused_digits if int(x) >= 5])
    else:
        return random.choice([x for x in unused_digits if int(x) < 5])
    


def do_suffle(secret):
    string_list = list(secret)
    random.shuffle(string_list)
    return ''.join(string_list)


def generate_unique_numbers():
    numbers = list(range(10))
    random.shuffle(numbers)
    unique_numbers = numbers[:4]
    return ''.join(map(str, unique_numbers))

def delete_bad_answer(hit, blow, challenge_number, answer_list):
    new_answer_list = []
    for answer in answer_list:
        [hit_temp, blow_temp] = get_hit_blow_count(answer, challenge_number)
        if hit == hit_temp and blow == blow_temp:
            new_answer_list.append(answer);
    return new_answer_list

def delete_bad_answer_high_low(high, low, answer_list):
    new_answer_list = []
    for answer in answer_list:
        [high_temp, low_temp] = get_high_low_count(answer)
        if high == high_temp and low == low_temp:
            new_answer_list.append(answer);
    return new_answer_list

def delete_bad_answer_target(number, position, answer_list):
    if position == -1:
        return answer_list
    new_answer_list = []
    for answer in answer_list:
        if number == answer[position]:
            new_answer_list.append(answer);
    return new_answer_list

def get_hit_blow_count(answer, challenge_number):
    hit, blow = 0, 0
    for digit_index, digit in enumerate(challenge_number):
        secret_index = answer.find(digit)
        if digit_index == secret_index:
            hit += 1
        elif secret_index > -1:
            blow += 1
    return [hit, blow]

def get_high_low_count(answer):
        high, low = 0, 0
        for digit in answer:
            if int(digit) > 4:
                high += 1
            else:
                low += 1
        return [high, low]


