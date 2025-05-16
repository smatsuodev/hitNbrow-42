from pydantic import BaseModel

from game.action.BaseAction import BaseAction


class BaseActionResult(BaseModel):
    action: BaseAction

    def as_body(self) -> dict:
        raise NotImplementedError()
