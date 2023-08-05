from typing import List, TypeVar, Generic

from model.enums import ConnectorEnum
from model.sql_column_operator import SqlColumnOperator
from utils import string_util

T = TypeVar("T")


class AbstractContainer(Generic[T]):
    def __init__(self, connector: str):
        self.connector = connector
        self.elements: List[T] = []

    def append(self, value: T):
        self.elements.append(value)

    def get_elements(self) -> List[T]:
        return self.elements

    def get_element(self, index: int) -> T:
        return self.elements[index]

    def get_connector(self) -> str:
        return self.connector

    @classmethod
    def build_and(cls):
        return cls(ConnectorEnum.AND.value)

    @classmethod
    def build_or(cls):
        return cls(ConnectorEnum.OR.value)

    def __repr__(self):
        return string_util.join_repr(self.connector, self.elements)


class SqlColumnOperatorContainer(AbstractContainer[SqlColumnOperator]):
    def __init__(self, connector: str):
        super(self.__class__, self).__init__(connector)

    def trans_to_sql(self):
        return [element.do_query() for element in self.elements]


class SqlColumnOperatorGroupContainer(AbstractContainer[SqlColumnOperatorContainer]):
    def __init__(self, connector: str):
        super(self.__class__, self).__init__(connector)
