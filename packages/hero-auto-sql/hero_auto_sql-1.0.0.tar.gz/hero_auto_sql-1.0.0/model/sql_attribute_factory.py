from typing import Dict

from model.enums import ColumnOperatorEnum
from model.sql_column_operator import SqlColumnOperator, EqSqlColumnOperator, GtSqlColumnOperator, \
    GteSqlColumnOperator, LtSqlColumnOperator, LteSqlColumnOperator


class SqlAttributeOperateFactory:
    __CLASS_MAP: Dict[str, SqlColumnOperator] = {
        ColumnOperatorEnum.EQ.value: EqSqlColumnOperator,
        ColumnOperatorEnum.GT.value: GtSqlColumnOperator,
        ColumnOperatorEnum.GTE.value: GteSqlColumnOperator,
        ColumnOperatorEnum.LT.value: LtSqlColumnOperator,
        ColumnOperatorEnum.LTE.value: LteSqlColumnOperator,
    }

    @classmethod
    def build(cls, operate_type: str) -> SqlColumnOperator:
        return cls.__CLASS_MAP[operate_type]
