from typing import Any


variables: dict[Any, Any] = {}


def get(key: str, default: Any = None) -> Any:
    return variables.get(key, default)


def set(key: str, value: Any) -> None:
    variables[key] = value


def remove(key: str) -> None:
    if key in variables.keys():
        variables.pop(key)


def clear() -> None:
    variables.clear()


def print_all() -> None:
    print(variables)