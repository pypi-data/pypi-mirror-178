from sqlalchemy.orm import scoped_session, sessionmaker

from model.enums import BehaviorEnum, ColumnOperatorEnum, ConnectorEnum
from model.sql_token import SqlToken
from sql_parser.sql_container_parse import SqlContainerParse
from sql_parser.token_parse import TokenParse
from test import engine, TestUser
from test.user import MysqlTestUser


def test_insert():
    session = scoped_session(sessionmaker(bind=engine, expire_on_commit=False))
    # session = sessionmaker(bind=engine, expire_on_commit=False)()

    # print(session2.__class__)
    mysql = MysqlTestUser(session)
    # mysql.delete_by_user_id_and_group_id(1, 1)
    mysql.delete_by_user_id_and_group_id(1, 1)

    session.add(TestUser(user_id=1, group_id=1, grade_no=1))
    session.commit()

    user = mysql.find_by_user_id_and_group_id(1, 1)
    print(user)


def test_token_parse_find_by_user_id_and_group_id_gt_or_grade_no_lt():
    element_list = [
        element
        for element in TokenParse.parse(
            "find_by_user_id_and_group_id_gt_or_grade_no_lt"
        )
    ]

    assert element_list[0].token_type == SqlToken.BEHAVIOR
    assert element_list[0].value == BehaviorEnum.FIND.value

    assert element_list[1].token_type == SqlToken.BY
    assert element_list[1].value == SqlToken.BY

    assert element_list[2].token_type == SqlToken.COLUMN
    assert element_list[2].value == "user_id"

    assert element_list[3].token_type == SqlToken.CONNECTOR
    assert element_list[3].value == ConnectorEnum.AND.value

    assert element_list[4].token_type == SqlToken.COLUMN
    assert element_list[4].value == "group_id"

    assert element_list[5].token_type == SqlToken.OPERATOR
    assert element_list[5].value == ColumnOperatorEnum.GT.value

    assert element_list[6].token_type == SqlToken.CONNECTOR
    assert element_list[6].value == ConnectorEnum.OR.value

    assert element_list[7].token_type == SqlToken.COLUMN
    assert element_list[7].value == "grade_no"

    assert element_list[8].token_type == SqlToken.OPERATOR
    assert element_list[8].value == ColumnOperatorEnum.LT.value


def test_token_parse_delete_by_user_id_and_group_id_gt_or_grade_no_lt():
    element_list = [
        element
        for element in TokenParse.parse(
            "delete_by_user_id_and_group_id_gt_or_grade_no_lt"
        )
    ]

    assert element_list[0].token_type == SqlToken.BEHAVIOR
    assert element_list[0].value == BehaviorEnum.DELETE.value

    assert element_list[1].token_type == SqlToken.BY
    assert element_list[1].value == SqlToken.BY

    assert element_list[2].token_type == SqlToken.COLUMN
    assert element_list[2].value == "user_id"

    assert element_list[3].token_type == SqlToken.CONNECTOR
    assert element_list[3].value == ConnectorEnum.AND.value

    assert element_list[4].token_type == SqlToken.COLUMN
    assert element_list[4].value == "group_id"

    assert element_list[5].token_type == SqlToken.OPERATOR
    assert element_list[5].value == ColumnOperatorEnum.GT.value

    assert element_list[6].token_type == SqlToken.CONNECTOR
    assert element_list[6].value == ConnectorEnum.OR.value

    assert element_list[7].token_type == SqlToken.COLUMN
    assert element_list[7].value == "grade_no"

    assert element_list[8].token_type == SqlToken.OPERATOR
    assert element_list[8].value == ColumnOperatorEnum.LT.value


def test_container_parse():
    behavior_token, group = SqlContainerParse.parse(
        "find_by_user_id_and_group_id", TestUser, (1, 2), {}
    )
    assert behavior_token.token_type == SqlToken.BEHAVIOR
    assert behavior_token.value == BehaviorEnum.FIND.value

    assert group.get_element(0).get_element(0).column == "user_id"
    assert group.get_element(0).get_element(0).value == 1

    assert group.get_element(0).get_element(1).column == "group_id"
    assert group.get_element(0).get_element(1).value == 2
