from model.sql_container import SqlColumnOperatorGroupContainer
from model.sql_token import SqlToken


class SqlContainerParseResult:

    behavior: SqlToken

    column_container: SqlColumnOperatorGroupContainer

    def __init__(self, behavior, column_container):
        self.behavior = behavior
        self.column_container = column_container
