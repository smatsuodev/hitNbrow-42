from collections import Counter
import random
from util import util


class ItemStrategyInput:
    def __init__(self, turn: int, can_use_item: bool, answer_list_oppo: list[str], secret: str):
        self.turn = turn
        self.can_use_item = can_use_item
        self.answer_list_oppo = answer_list_oppo
        self.secret = secret

class ItemStrategyOutput:
    def __init__(self, messageType: str, action: str, number: str | None = None, new_secret: str | None = None,
                 new_answer_list_oppo: list[str] | None = None):
        self.messageType = messageType
        self.action = action
        self.number = number
        self.new_secret = new_secret
        self.new_answer_list_oppo = new_answer_list_oppo

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
    def __init__(self, danger: int, warning:int):
        self._danger = danger
        self._warning = warning

    def execute(self, input_data):
        if (input_data.can_use_item and input_data.turn == 1):
            if (self._use_high_low()):
                return self.response_highlow()
            elif (self._use_target()):
                return self.response_target("5") 

        elif (input_data.can_use_item and input_data.turn == 2):
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
    
    def _do_change(self, answer_list_oppo: list[str], secret: str) -> tuple[str, int, str | None]:
        all_digits = set(map(str, range(10)))
        secret_list = set(secret)
        unused_digits_set = all_digits - secret_list
        unused_digits = list(map(int,unused_digits_set))
        digit_count = Counter()
        for ans in answer_list_oppo:
            for digit in ans:
                digit_count[digit] += 1
        most_frequent_digit = max(digit_count, key=digit_count.get)
        is_high = int(most_frequent_digit) >= 5
        for i in range(len(secret)):
            if (secret[i] == most_frequent_digit):
                new_num = random.choice(list(filter(lambda x: x >= 5 if is_high else x < 5, unused_digits)))
                new_secret = secret[:i] + str(new_num) + secret[i+1:]
                return (new_secret, i, "high" if is_high else "low")
        return (secret, -1, None)
    
    def _do_shuffle(self, secret: str) -> str:
        secret_list = list(secret)
        random.shuffle(secret_list)
        return ''.join(secret_list)