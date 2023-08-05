from model.enums import ColumnOperatorEnum, ConnectorEnum
from model.sql_attribute_factory import SqlAttributeOperateFactory
from model.sql_container import (
    SqlColumnOperatorGroupContainer,
    SqlColumnOperatorContainer,
)
from model.sql_container_parse_result import SqlContainerParseResult
from model.sql_token import SqlToken
from sql_parser.token_parse import TokenParse


class SqlContainerParse:

    @classmethod
    def parse(
        cls,
        function_name: str,
        mysql_class,
        params_list: tuple,
        params_dict: dict,
    ) -> SqlContainerParseResult:
        """
        解析函数为可组装sqlalchemy的元素
        :param function_name:   函数名称
        :param mysql_class:     数据库对象
        :param params_list:     下标参数列表
        :param params_dict:     kv参数列表
        :return:
        """
        # 临时column存储
        column_token = None
        column_index = 0
        # 临时column操作符
        operator_token = None
        # 本次行为，是删除还是查询
        behavior = None

        group = SqlColumnOperatorGroupContainer.build_or()
        current_attributes = SqlColumnOperatorContainer.build_and()
        group.append(current_attributes)
        for index, sql_token in enumerate(TokenParse.parse(function_name)):
            if index == 0:
                # catch behavior
                behavior = sql_token
                continue
            if index == 1:
                # pass by
                continue
            if sql_token.token_type == SqlToken.CONNECTOR:
                current_attributes.append(
                    cls.__build_sql_attribute(
                        column_token,
                        operator_token,
                        column_index,
                        mysql_class,
                        params_list,
                        params_dict,
                    )
                )
                # clear 临时数据
                column_token = None
                operator_token = None
                column_index += 1
                if sql_token.value == ConnectorEnum.OR.value:
                    current_attributes = SqlColumnOperatorContainer.build_and()
                    group.append(current_attributes)
            elif sql_token.token_type == SqlToken.COLUMN:
                column_token = sql_token
            elif sql_token.token_type == SqlToken.OPERATOR:
                operator_token = sql_token
        if column_token is not None:
            current_attributes.append(
                cls.__build_sql_attribute(
                    column_token,
                    operator_token,
                    column_index,
                    mysql_class,
                    params_list,
                    params_dict,
                )
            )

        return SqlContainerParseResult(behavior, group)

    @classmethod
    def __get_column_value(
        cls,
        column_token: SqlToken,
        column_index: int,
        params_list: tuple,
        params_dict: dict,
    ):
        if column_index < len(params_list):
            return params_list[column_index]
        return params_dict.get(column_token.value)

    @classmethod
    def __build_sql_attribute(
        cls,
        column_token: SqlToken,
        operator_token: SqlToken,
        column_index: int,
        mysql_class,
        params_list: tuple,
        params_dict: dict,
    ):
        column_operator_type = (
            operator_token.value
            if operator_token is not None
            else ColumnOperatorEnum.EQ.value
        )
        operator_class = SqlAttributeOperateFactory.build(column_operator_type)
        return operator_class(
            column=column_token.value,
            value=cls.__get_column_value(
                column_token, column_index, params_list, params_dict
            ),
            mysql_class=mysql_class,
        )
