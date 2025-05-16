from util.commonUtils import create_unique_list


class ChallengeCandidateInput():
    def __init__(self, answerList: list[str]):
        self.answerList = answerList
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
        return input.answerList