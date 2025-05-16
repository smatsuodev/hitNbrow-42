from __future__ import annotations
from pydantic import BaseModel

from util.number_validate import NUMBER_DIGITS


class ChallengeResult(BaseModel):
    hit: int
    blow: int


class HighLowResult(BaseModel):
    high: int
    low: int


class SecretNumber(BaseModel):
    number: str

    def get_hit_blow_count(self, challenge_number: str) -> ChallengeResult:
        hit, blow = 0, 0
        for digit_index, digit in enumerate(challenge_number):
            secret_index = self.number.find(digit)
            if digit_index == secret_index:
                hit += 1
            elif secret_index > -1:
                blow += 1
        return ChallengeResult(hit=hit, blow=blow)

    def get_high_low_count(self) -> HighLowResult:
        high, low = 0, 0
        for digit in self.number:
            if int(digit) > 4:
                high += 1
            else:
                low += 1
        return HighLowResult(high=high, low=low)

    def get_number_index(self, target: str) -> int:
        return self.number.find(target)

    def check_valid_change_number(self, changed: str) -> [bool, int, bool]:
        changed_digit_position: int | None = None
        changed_is_high = False

        def is_high(digit: str) -> bool:
            return int(digit) > 4

        for idx, (prev, new) in enumerate(zip(self.number, changed)):
            if prev != new:
                if changed_digit_position is not None:
                    return [False, -1, False]
                if is_high(prev) ^ is_high(new):
                    return [False, -1, False]
                changed_digit_position = idx
                changed_is_high = is_high(new)

        if changed_digit_position is None:
            return [False, -1, False]

        return [True, changed_digit_position, changed_is_high]

    def check_valid_shuffle_number(self, shuffled: str) -> bool:
        count = self.get_hit_blow_count(shuffled)
        return (count.hit + count.blow) == NUMBER_DIGITS
