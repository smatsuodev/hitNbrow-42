from pydantic import BaseModel

from util.case import snake_to_camel


class BaseRecvModel(BaseModel):
    class Config:
        alias_generator = snake_to_camel
        regex_engine = 'python-re'
        use_enum_values = True
        populate_by_name = True


class BaseRecvMessage(BaseRecvModel):
    message_type: str
    body: dict

