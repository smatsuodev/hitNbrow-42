from collections import Counter
import math
import random
import sys
from util import util

DEFAULT_STRATEGY = "default"

def factory_item_strategy(type: str):
    """
    戦略のファクトリメソッド
    """
    if type == "default":
        return DefaultItemStrategy()
    elif type == "no_item_in_first_turn":
        return NoItemInFirstTurnItemStrategy()
    elif type == "use_target_after_shuffle":
        return UseTargetAfterShuffleStrategy()
    else:
        raise ValueError("Unknown strategy type")

class ItemStrategyInput:
    def __init__(self, action_turn: int, can_use_item: bool, answer_list_oppo: list[str], secret: str, game_turn: int, answer_list: list[str],
                 can_oppo_use_shuffle: bool = False, can_oppo_use_target: bool = False,
                 oppo_last_target: dict | None = None):
        self.action_turn = action_turn
        self.can_use_item = can_use_item
        self.answer_list_oppo = answer_list_oppo
        self.secret = secret
        self.game_turn = game_turn
        self.answer_list = answer_list
        self.can_oppo_use_shuffle = can_oppo_use_shuffle
        self.can_oppo_use_target = can_oppo_use_target
        self.oppo_last_target = oppo_last_target

class ItemStrategyOutput:
    def __init__(self, messageType: str, action: str, number: str | None = None, new_secret: str | None = None,
                 new_answer_list_oppo: list[str] | None = None, oppo_last_target: dict | None = None):
        self.messageType = messageType
        self.action = action
        self.number = number
        self.new_secret = new_secret
        self.new_answer_list_oppo = new_answer_list_oppo
        self.oppo_last_target = oppo_last_target

    def did_use_item(self) -> bool:
        return self.action != "pass"

    def as_body(self) -> dict:
        base = {
            "messageType": self.messageType,
            "body": {
                "action": self.action,
            }
        }
        if self.number is not None:
            base["body"]["number"] = self.number
        return base

class ItemStrategy:
    def __init__(self):
        self.can_use_target = True
        self.can_use_high_low = True
        self.can_use_shuffle = True
        self.can_use_change = True
        self.turn = 0

    def setup(self):
        self.can_use_target = True
        self.can_use_high_low = True
        self.can_use_shuffle = True
        self.can_use_change = True

    def teardown(self):
        pass

    def _use_shuffle(self):
        if self.can_use_shuffle:
            self.can_use_shuffle = False
            return True
        
        return False
    
    def _use_target(self):
        if self.can_use_target:
            self.can_use_target = False
            return True
        
        return False
    
    def _use_high_low(self):
        if self.can_use_high_low:
            self.can_use_high_low = False
            return True
        
        return False
    
    def _use_change(self):
        if self.can_use_change:
            self.can_use_change = False
            return True
        
        return False

    def response_highlow(self):
        return ItemStrategyOutput(
            messageType='requestItemAction-high-low',
            action="high-low",
        )
    
    def response_target(self, target: str):
        return ItemStrategyOutput(
            messageType='requestItemAction-target',
            action="target",
            number=target,
        )
    
    def response_change(self, secret: str, new_answer_list_oppo: list[str]):
        return ItemStrategyOutput(
            messageType='requestItemAction-change',
            action="change",
            number=secret,
            new_secret=secret,
            new_answer_list_oppo=new_answer_list_oppo,
        )
    
    def response_shuffle(self, secret: str, new_answer_list_oppo: list[str]):
        return ItemStrategyOutput(
            messageType='requestItemAction-shuffle',
            action="shuffle",
            number=secret,
            new_secret=secret,
            new_answer_list_oppo=new_answer_list_oppo,
        )
    
    def response_pass(self):
        return ItemStrategyOutput(
            messageType='requestItemAction-pass',
            action="pass",
        )

    def execute(self, input_data: ItemStrategyInput) -> ItemStrategyOutput:
        pass


class DefaultItemStrategy(ItemStrategy):
    def __init__(self):
        self._danger = 500
        self._warning = 1000

    def execute(self, input_data):
        if (input_data.can_use_item and input_data.action_turn == 1):
            if (self._use_high_low()):
                return self.response_highlow()
            elif (self._use_target()):
                return self.response_target(self._do_target(input_data.answer_list)) 

        elif (input_data.can_use_item and input_data.action_turn == 2):
            if len(input_data.answer_list_oppo) <= self._danger and self._use_change():
                new_secret, pos, highlow = self._do_change(input_data.answer_list_oppo, input_data.secret)
                new_answer_list_oppo = input_data.answer_list_oppo
                if highlow is not None:
                    new_answer_list_oppo = util.add_change(input_data.answer_list_oppo, pos, highlow)
                return self.response_change(new_secret, new_answer_list_oppo)

            if len(input_data.answer_list_oppo) <= self._warning and self._use_shuffle():
                new_secret = self._do_shuffle(input_data.secret)
                new_answer_list_oppo = util.add_shuffle(input_data.answer_list_oppo)
                return self.response_shuffle(new_secret, new_answer_list_oppo)

        return self.response_pass()

    def _get_change_candidates(self, answer_list_oppo: list[str], secret: str) -> str | None:
        is_high_at_pos = {i: answer_list_oppo[0][i] >= 5 for i in range(4) }
        for ans in answer_list_oppo:
            for i in range(4):
                if ans[i] >= 5 != is_high_at_pos[i]:
                    is_high_at_pos[i] = None

        index_cands = set()
        for i in range(4):
            if is_high_at_pos[i] is not None:
                index_cands.add(i)
        
        if len(index_cands) == 0:
            return None
        
        # max_
        # for ans in answer_list_oppo:
        #     for i in index_cands:

        
    
    def _do_change(self, answer_list_oppo: list[str], secret: str) -> tuple[str, int, str | None]:
        all_digits = set(map(str, range(10)))
        secret_list = set(secret)
        unused_digits_set = all_digits - secret_list
        unused_digits = list(map(int,unused_digits_set))
        unused_high_digits = list(filter(lambda x: x >= 5, unused_digits))
        unused_low_digits = list(filter(lambda x: x < 5, unused_digits))
        digit_count = Counter()
        for ans in answer_list_oppo:
            for digit in ans:
                if digit in secret:
                    digit_count[digit] += 1
        most_frequent_digit = max(digit_count, key=digit_count.get)
        high_digit_count = {i: digit_count[i] for i in unused_high_digits}
        low_digit_count = {i: digit_count[i] for i in unused_low_digits}
        worst_frequent_digit_in_high = min(high_digit_count, key=high_digit_count.get)
        worst_frequent_digit_in_low = min(low_digit_count, key=low_digit_count.get)
        is_high = int(most_frequent_digit) >= 5
        new_num = worst_frequent_digit_in_high if is_high else worst_frequent_digit_in_low
        for i in range(len(secret)):
            if (secret[i] == most_frequent_digit):
                new_num = random.choice(list(filter(lambda x: x >= 5 if is_high else x < 5, unused_digits)))
                new_secret = secret[:i] + str(new_num) + secret[i+1:]
                return (new_secret, i, "high" if is_high else "low")
        raise ValueError("No change possible")
    
    def _do_shuffle(self, secret: str) -> str:
        secret_list = list(secret)
        random.shuffle(secret_list)
        return ''.join(secret_list)
    
    def _calculate_entropy(self, hist: Counter) -> float:
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
                pass

        return best_target


class NoItemInFirstTurnItemStrategy(DefaultItemStrategy):
    def __init__(self):
        self._danger = 500
        self._warning = 1000

    def execute(self, input_data: ItemStrategyInput) -> ItemStrategyOutput:
        if (input_data.game_turn == 1):
            return self.response_pass()
        if (input_data.can_use_item and input_data.action_turn == 1):
            if (self._use_high_low()):
                return self.response_highlow()
            elif (self._use_target()):
                return self.response_target("5") 

        elif (input_data.can_use_item and input_data.action_turn == 2):
            if len(input_data.answer_list_oppo) <= self._danger and self._use_change():
                new_secret, pos, highlow = self._do_change(input_data.answer_list_oppo, input_data.secret)
                new_answer_list_oppo = input_data.answer_list_oppo
                if highlow is not None:
                    new_answer_list_oppo = util.add_change(input_data.answer_list_oppo, pos, highlow)
                return self.response_change(new_secret, new_answer_list_oppo)

            if len(input_data.answer_list_oppo) <= self._warning and self._use_shuffle():
                new_secret = self._do_shuffle(input_data.secret)
                new_answer_list_oppo = util.add_shuffle(input_data.answer_list_oppo)
                return self.response_shuffle(new_secret, new_answer_list_oppo)

        return self.response_pass()

class UseTargetAfterShuffleStrategy(DefaultItemStrategy):
    def execute(self, input_data: ItemStrategyInput) -> ItemStrategyOutput:
        if (not input_data.can_oppo_use_shuffle and self._use_target()):
            return self.response_target(self._do_target(input_data.answer_list))
        
        if (not input_data.can_oppo_use_target
            and int(input_data.oppo_last_target["position"]) >= 0
            and self._use_change()
            ):
            number = input_data.oppo_last_target["number"]
            pos = input_data.oppo_last_target["position"]
            print(f"number: {number}, pos: {pos}", file=sys.stderr)
            is_high = number >= 5
            unused_digits = set(map(str, range(10))) - set(input_data.secret)
            new_num = random.choice(list(filter(lambda x: x >= 5 if is_high else x < 5, map(int, unused_digits))))
            new_secret = input_data.secret[:pos] + str(new_num) + input_data.secret[pos+1:]
            highlow = "high" if is_high else "low"
            new_answer_list_oppo = util.add_change(input_data.answer_list_oppo, pos, highlow)
            return self.response_change(new_secret, new_answer_list_oppo)
        
        if (input_data.can_use_item and input_data.action_turn == 1):
            if (self._use_high_low()):
                return self.response_highlow()
        elif (input_data.can_use_item and input_data.action_turn == 2):
            if len(input_data.answer_list_oppo) <= self._danger and self._use_change():
                new_secret, pos, highlow = self._do_change(input_data.answer_list_oppo, input_data.secret)
                new_answer_list_oppo = input_data.answer_list_oppo
                if highlow is not None:
                    new_answer_list_oppo = util.add_change(input_data.answer_list_oppo, pos, highlow)
                return self.response_change(new_secret, new_answer_list_oppo)

            if len(input_data.answer_list_oppo) <= self._warning and self._use_shuffle():
                new_secret = self._do_shuffle(input_data.secret)
                new_answer_list_oppo = util.add_shuffle(input_data.answer_list_oppo)
                return self.response_shuffle(new_secret, new_answer_list_oppo)

        return self.response_pass()
    