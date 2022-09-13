from __future__ import annotations
from typing import Generic, TypeVar, Callable, final

from .adt import adt


T = TypeVar("T")
U = TypeVar("U")
_NO_DEFAULT = object()

@adt
@final
class Maybe(Generic[T]):
    just: (T,)
    nothing: ()

    def apply(self, func: Callable[[T], U]) -> Maybe[U]:
        match self:
            case Maybe.just(val):
                return Maybe.just(func(val))
            case Maybe.nothing():
                return self


    def unwrap(self, *, default: T=_NO_DEFAULT) -> T:
        match self:
            case Maybe.just(val):
                return val
            case Maybe.nothing():
                if default is _NO_DEFAULT:
                    raise TypeError("Attempted to unwrap Maybe.nothing(); can only unwrap Maybe.just(val)")
                return default

    def __repr__(self):
        match self:
            case Maybe.just(val):
                return f"<Maybe.just: {val!r}>"
            case Maybe.nothing():
                return "<Maybe.nothing>"

    def __eq__(self, other):
        match (self, other):
            case (Maybe.just(val), Maybe.just(other_val)):
                return val == other_val
            case (Maybe.nothing(), Maybe.nothing()):
                return True
            case Maybe.just(_), Maybe.nothing(): 
                return False
            case Maybe.nothing(), Maybe.just(_): 
                return False
            case _:
                return NotImplemented

    def __hash__(self):
        match self:
            case Maybe.just(val):
                return hash(val)
            case Maybe.nothing():
                return hash(repr(self))
