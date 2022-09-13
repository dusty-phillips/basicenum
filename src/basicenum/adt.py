from __future__ import annotations
from typing import Any, Type, Callable
import types
import inspect


def make_init(name: str, annotations: tuple) -> Callable[..., None]:
    """
    Create an initializer function for the individual datatype.
    """

    def __init__(self, *args: Any) -> None:
        if len(args) != len(annotations):
            raise TypeError(
                f"{name}() takes exactly {len(annotations)} arguments ({len(args)} given)"
            )

        for index, arg in enumerate(args):
            setattr(self, f"_{index}", arg)

    return __init__


def adt(cls):
    """
    Construct an algebraic datatype.

    For usage, consider the maybe.py datatype.
    """
    annotations = inspect.get_annotations(cls, eval_str=True)
    print(annotations)

    for name, annotation in annotations.items():
        nc: Type[cls] = types.new_class(name, bases=(cls,))

        nc.__qualname__ = f"{cls.__qualname__}.{name}"
        nc.__init__ = make_init(nc.__qualname__, annotation)
        nc.__match_args__: tuple[str, ...] = tuple((f"_{index}" for index in range(len(annotations))))  # type: ignore
        setattr(cls, name, nc)

    return cls
