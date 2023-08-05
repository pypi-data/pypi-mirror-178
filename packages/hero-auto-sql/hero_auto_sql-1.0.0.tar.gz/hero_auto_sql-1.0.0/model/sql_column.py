import sqlalchemy


class SqlColumn:
    """
    SQL字段，不包含值
    """

    def __init__(
        self,
        column: str,
        mysql_class: sqlalchemy.orm.decl_api.DeclarativeMeta,
    ):
        self.column = column
        self.mysql_class = mysql_class

    def get_attribute(self):
        return self.mysql_class.__dict__[self.column]
