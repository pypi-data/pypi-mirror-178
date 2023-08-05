from enum import Enum
from typing import TypeVar, Optional

T = TypeVar("T")


class EnumUtil:
    @classmethod
    def get(cls, enum: Enum, value: T) -> Optional[T]:
        for enum_element in enum:
            if enum_element.value == value:
                return value
        return None
