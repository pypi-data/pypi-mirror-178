from typing import (
    Any,
    Callable,
)

def dumps(
    obj: Any,
    ensure_ascii: bool = ...,
    double_precision: int = ...,
    indent: int = ...,
    orient: str = ...,
    date_unit: str = ...,
    iso_dates: bool = ...,
    default_handler: None
    | Callable[[Any], str | float | bool | list | dict | None] = ...,
) -> str: ...
def loads(
    s: str,
    precise_float: bool = ...,
    numpy: bool = ...,
    dtype: None = ...,
    labelled: bool = ...,
) -> Any: ...
