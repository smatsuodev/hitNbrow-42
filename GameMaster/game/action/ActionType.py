from enum import Enum


class ActionType(Enum):
    Challenge = "challenge"
    Pass = "pass"
    Target = "target"
    HighLow = "high-low"
    Shuffle = "shuffle"
    Change = "change"
