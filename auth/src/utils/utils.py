from enum import Enum
from typing import Any


def get_column_name(column_name: str):
    return column_name.split(".")[-1]


def dict_factory(data: list[tuple[str, Any]]) -> dict[str, Any]:
    return {
        key: value.value if isinstance(value, Enum) else value
        for key, value in data
        if value is not None
    }
