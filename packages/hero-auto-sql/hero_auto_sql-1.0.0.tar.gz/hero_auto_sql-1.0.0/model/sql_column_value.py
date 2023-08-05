import sqlalchemy

from model.sql_column import SqlColumn


class SqlColumnValue(SqlColumn):
    """
    SQL字段，包含某个字段对应什么值
    """

    def __init__(
        self,
        column: str,
        value: object,
        mysql_class: sqlalchemy.orm.decl_api.DeclarativeMeta,
    ):
        super().__init__(column, mysql_class)
        self.value = value

    def __repr__(self):
        return f"<column:{self.column}, value:{self.value}>"
