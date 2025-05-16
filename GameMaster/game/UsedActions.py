from game.action.ActionType import ActionType


class UsedActions:
    def __init__(self):
        self.used_list = []

    def append(self, action: ActionType):
        if action == ActionType.Pass or action == ActionType.Challenge:
            return
        if action in self.used_list:
            raise ValueError(f"action {action} is already used.")
        self.used_list.append(action)

    def clear(self):
        self.used_list.clear()
