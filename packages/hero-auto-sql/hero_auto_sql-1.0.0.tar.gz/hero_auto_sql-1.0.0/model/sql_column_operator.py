from abc import ABCMeta, abstractmethod

import sqlalchemy
from sqlalchemy.orm import Session

from model.sql_column_value import SqlColumnValue


class SqlColumnOperator(SqlColumnValue, metaclass=ABCMeta):
    """
    SQL中用于查询的熟悉
    """

    def __init__(
        self,
        column: str,
        value: object,
        mysql_class: sqlalchemy.orm.decl_api.DeclarativeMeta,
    ):
        super().__init__(column, value, mysql_class)

    @abstractmethod
    def do_query(self):
        ...


class EqSqlColumnOperator(SqlColumnOperator):
    def __init__(
        self,
        column: str,
        value: object,
        mysql_class: sqlalchemy.orm.decl_api.DeclarativeMeta,
    ):
        super(self.__class__, self).__init__(column, value, mysql_class)

    def do_query(self):
        return self.get_attribute() == self.value


class LtSqlColumnOperator(SqlColumnOperator):
    def __init__(
        self,
        column: str,
        value: object,
        mysql_class: sqlalchemy.orm.decl_api.DeclarativeMeta,
    ):
        super(self.__class__, self).__init__(column, value, mysql_class)

    def do_query(self):
        return self.get_attribute() < self.value


class LteSqlColumnOperator(SqlColumnOperator):
    def __init__(
        self,
        column: str,
        value: object,
        mysql_class: sqlalchemy.orm.decl_api.DeclarativeMeta,
    ):
        super(self.__class__, self).__init__(column, value, mysql_class)

    def do_query(self):
        return self.get_attribute() <= self.value


class GtSqlColumnOperator(SqlColumnOperator):
    def __init__(
        self,
        column: str,
        value: object,
        mysql_class: sqlalchemy.orm.decl_api.DeclarativeMeta,
    ):
        super(self.__class__, self).__init__(column, value, mysql_class)

    def do_query(self):
        return self.get_attribute() > self.value


class GteSqlColumnOperator(SqlColumnOperator):
    def __init__(
        self,
        column: str,
        value: object,
        mysql_class: sqlalchemy.orm.decl_api.DeclarativeMeta,
    ):
        super(self.__class__, self).__init__(column, value, mysql_class)

    def do_query(self):
        return self.get_attribute() >= self.value
