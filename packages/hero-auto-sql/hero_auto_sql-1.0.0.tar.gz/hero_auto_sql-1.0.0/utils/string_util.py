from typing import List


def join_repr(connector: str, elements: List[object]) -> str:
    string_list = [element.__repr__() for element in elements]
    return connector.join(string_list)
