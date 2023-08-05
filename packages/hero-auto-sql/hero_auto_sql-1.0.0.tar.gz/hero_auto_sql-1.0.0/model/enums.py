from enum import Enum


class BehaviorEnum(Enum):
    """
    SQL行为定义
    """

    DELETE = "delete"
    FIND = "find"
    GET = "get"


class ConnectorEnum(Enum):
    """
    sql连接组的富豪
    """

    AND = "and"
    OR = "or"


class ColumnOperatorEnum(Enum):
    """
    支持的DML运算符
    """

    EQ = "eq"
    LT = "lt"
    LTE = "lte"
    GT = "gt"
    GTE = "gte"