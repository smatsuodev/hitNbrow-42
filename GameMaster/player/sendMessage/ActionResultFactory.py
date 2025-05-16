from game.action.ActionType import ActionType
from game.actionResult.BaseActionResult import BaseActionResult
from player.sendMessage.BaseSendMessage import BaseSendMessage
from player.sendMessage.SendChallengeResult import SendChallengeResult
from player.sendMessage.SendChangeResult import SendChangeResult
from player.sendMessage.SendHighLowResult import SendHighLowResult
from player.sendMessage.SendPassResult import SendPassResult
from player.sendMessage.SendShuffleResult import SendShuffleResult
from player.sendMessage.SendTargetResult import SendTargetResult


class ActionResultFactory:
    @staticmethod
    def create_from(result: BaseActionResult) -> BaseSendMessage:
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

