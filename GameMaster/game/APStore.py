from game.action.ActionType import ActionType

AP_DICT: dict[ActionType, int] = {
    ActionType.Challenge: 1,
    ActionType.Target: 5,
    ActionType.HighLow: 8,
    ActionType.Shuffle: 9,
    ActionType.Change: 6,
}


class APStore:
    def __init__(self):
        self.current_ap = 0

    def did_action(self, action: ActionType):
        ap = AP_DICT[action]
        self.current_ap += ap if ap is not None else 0

    def clear(self):
        self.current_ap = 0
