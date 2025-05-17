from util.util import create_unique_list

def factory_challenge_candidate_strategy(type: str):
    """
    戦略のファクトリメソッド
    """
    if type == "brute_force":
        return BluteForceStrategy()
    elif type == "pick_from_answer":
        return PickFromAnswerStrategy()
    elif type == "fixed_first_candidate":
        return FixedFirstCandidateStrategy()
    else:
        raise ValueError("Unknown strategy type")


class ChallengeCandidateInput():
    def __init__(self, answer_list: list[str], game_turn: int):
        self.answer_list = answer_list
        self.game_turn = game_turn
        pass

class ChallengeCandidateStrategy():
    def __init__(self):
        pass

    def candidates(self, input: ChallengeCandidateInput) -> list[str]:
        pass

class BluteForceStrategy(ChallengeCandidateStrategy):
    def __init__(self):
        super().__init__()

    def candidates(self, input: ChallengeCandidateInput) -> list[str]:
        """
        全ての候補を返す
        """
        return create_unique_list()
    
class PickFromAnswerStrategy(ChallengeCandidateStrategy):
    def __init__(self):
        super().__init__()

    def candidates(self, input: ChallengeCandidateInput) -> list[str]:
        """
        答えの候補から選ぶ（＝4H0B狙い）
        """
        return input.answer_list

class FixedFirstCandidateStrategy(ChallengeCandidateStrategy):
    def __init__(self):
        super().__init__()
        self.fixed_number = "0123"

    def candidates(self, input: ChallengeCandidateInput) -> list[str]:
        """
        固定の数字を持つ候補を返す
        """
        if input.game_turn == 1:
            return [self.fixed_number]
        
        return input.answer_list