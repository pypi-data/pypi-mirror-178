import functools
from typing import List

from sqlalchemy import or_, and_
from sqlalchemy.orm import Query

from model.enums import BehaviorEnum
from model.type_defind import Validate_Session
from sql_parser.sql_container_parse import SqlContainerParse
from utils.enum_util import EnumUtil

DEFAULT_MYSQL_SESSION = "mysql_session"
DEFAULT_MYSQL_CLASS = "__mysql_class__"


def do_find_execute(query: Query) -> List:
    return query.all()


def do_delete_execute(query: Query) -> int:
    return query.delete()


def construct_extra_query(query: Query, limit: int = None, offset: int = None):
    if limit is not None:
        query = query.limit(limit)
    if offset is not None:
        query = query.offset(offset)
    return query


def do_execute(session: Validate_Session, mysql_class, func, *args, **kwargs):
    function_name = func.__name__
    parse_result = SqlContainerParse.parse(
        function_name, mysql_class, args, kwargs
    )
    behavior_enum = EnumUtil.get(BehaviorEnum, parse_result.behavior.value)
    and_elements = []
    for sql_element in parse_result.column_container.get_elements():
        and_elements.append(and_(*sql_element.trans_to_sql()))
    query = session.query(mysql_class).filter(or_(*and_elements))
    if (
        behavior_enum == BehaviorEnum.GET.value
        or behavior_enum == BehaviorEnum.FIND.value
    ):
        return do_find_execute(query)
    elif behavior_enum == BehaviorEnum.DELETE.value:
        affect_rows = do_delete_execute(query)
        session.commit()
        return affect_rows
    return None


def get_session_and_mysql_class(
    call_object: object, default_session: str, validate: bool = False
) -> (Validate_Session, object):
    session_name = default_session
    session = call_object.__dict__[session_name]
    mysql_class = call_object.__class__.__dict__[DEFAULT_MYSQL_CLASS]
    if validate and not isinstance(session, Validate_Session):
        raise Exception("invalid session")
    return session, mysql_class


def auto_sql(func=None, default_session: str = DEFAULT_MYSQL_SESSION):
    # 将参数传给自身返回带参数的装饰器
    if func is None:
        return functools.partial(auto_sql, default_session=default_session)
        # def ooo(func):
        #     return auto_sql(func=func, default_session=default_session)
        # return ooo

    # 实际的装饰器
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        call_object = args[0]
        session, mysql_class = get_session_and_mysql_class(call_object, default_session)
        return do_execute(session, mysql_class, func, *args[1:], **kwargs)

    return wrapper
