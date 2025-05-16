from typing import override

from pydantic import BaseModel
from util.case import snake_to_camel


class BaseSendModel(BaseModel):
    class Config:
        alias_generator = snake_to_camel
        regex_engine = 'python-re'
        use_enum_values = True
        populate_by_name = True


class BaseSendMessage(BaseSendModel):
    state: str
    message_type: str
    body: dict

    def json(self) -> str:
        return self.model_dump_json(by_alias=True)
