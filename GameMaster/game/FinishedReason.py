from enum import IntEnum, auto


class FinishedReason(IntEnum):
    initialize_error = auto()
    invalid_secret = auto()
    invalid_action = auto()
    all_hit = auto()
    timeout = auto()

