class SqlToken:
    # 行为，比如find,get,delete
    BEHAVIOR = "behavior"
    # 占位符
    BY = "by"

    # sql 字段
    COLUMN = "column"
    # 连接符号
    CONNECTOR = "connector"
    # 操作符
    OPERATOR = "operator"

    def __init__(self, token_type: str, value: str):
        self.token_type = token_type
        self.value = value

    def __repr__(self):
        return f"token_type:{self.token_type}, value:{self.value}"
