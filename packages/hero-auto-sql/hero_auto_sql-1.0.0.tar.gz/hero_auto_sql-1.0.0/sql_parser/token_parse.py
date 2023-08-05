from typing import List

from model.enums import ColumnOperatorEnum, ConnectorEnum
from model.sql_token import SqlToken
from utils.enum_util import EnumUtil


class TokenValuePayLoad:
    def __init__(self):
        self.__text = ""
        self.__index = 0

    def append(self, value: str):
        if self.__index == 0:
            self.__text += value
        else:
            self.__text += f"_{value}"
        self.__index += 1

    def clear(self):
        self.__text = ""
        self.__index = 0

    def get_text(self):
        return self.__text

    def is_empty(self):
        return self.__index == 0


class TokenParse:
    @classmethod
    def parse(cls, function_name: str, spliter: str = "_") -> List[SqlToken]:
        tokens = function_name.split(spliter)
        token_value = TokenValuePayLoad()
        for index, token in enumerate(tokens):
            if index == 0:
                yield SqlToken(SqlToken.BEHAVIOR, token)
                continue
            if index == 1:
                if token == SqlToken.BY:
                    yield SqlToken(SqlToken.BY, SqlToken.BY)
                    continue
                else:
                    raise Exception("语法不对")
            if EnumUtil.get(ColumnOperatorEnum, token):
                if not token_value.is_empty():
                    yield SqlToken(SqlToken.COLUMN, token_value.get_text())
                yield SqlToken(SqlToken.OPERATOR, token)
                token_value.clear()
                continue
            if EnumUtil.get(ConnectorEnum, token):
                if not token_value.is_empty():
                    yield SqlToken(SqlToken.COLUMN, token_value.get_text())
                yield SqlToken(SqlToken.CONNECTOR, token)
                token_value.clear()
                continue
            token_value.append(token)
        if not token_value.is_empty():
            yield SqlToken(SqlToken.COLUMN, token_value.get_text())
