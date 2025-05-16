from game.action.ActionType import ActionType
from game.actionResult.BaseActionResult import BaseActionResult
from viewer.message.BaseMessage import BaseMessage
from viewer.message.SendChallengeResult import SendChallengeResult
from viewer.message.SendChangeResult import SendChangeResult
from viewer.message.SendHighLowResult import SendHighLowResult
from viewer.message.SendPassResult import SendPassResult
from viewer.message.SendShuffleResult import SendShuffleResult
from viewer.message.SendTargetResult import SendTargetResult


class ActionResultFactory:
    @staticmethod
    def create_from(result: BaseActionResult) -> BaseMessage:
        match result.action.actionType:
            case ActionType.Challenge:
                return SendChallengeResult(result=result)
            case ActionType.Pass:
                return SendPassResult(result=result)
            case ActionType.Target:
                return SendTargetResult(result=result)
            case ActionType.HighLow:
                return SendHighLowResult(result=result)
            case ActionType.Shuffle:
                return SendShuffleResult(result=result)
            case ActionType.Change:
                return SendChangeResult(result=result)
            case _:
                raise ValueError()

