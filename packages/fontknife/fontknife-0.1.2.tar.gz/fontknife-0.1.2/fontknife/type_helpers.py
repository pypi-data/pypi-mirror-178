from typing import overload, Union, Callable, TypeVar, Iterable, Optional

T = TypeVar('T')
SelectorCallable = Union[Callable[[T, ...], T], Callable[[Iterable[T]], T]]


@overload
def _select_not_none(chooser: SelectorCallable, candidates: Iterable[T]) -> T:
    return _select_not_none(chooser, *candidates)


@overload
def _select_not_none(chooser: SelectorCallable, *candidates: T) -> T:
    return _select_not_none(chooser, *candidates)


def _select_not_none(chooser: SelectorCallable, *candidates: Optional[T]) -> T:
    if len(candidates) == 1:
        candidates = candidates[0]
    return chooser(tuple(filter_none(candidates)))


@overload
def max_not_none(candidates: Iterable[Optional[T]]) -> T:
    return max_not_none(*candidates)


@overload
def max_not_none(*candidates: Optional[T]) -> T:
    return max_not_none(*candidates)


def max_not_none(*candidates: Optional[T]) -> T:
    return _select_not_none(max, *candidates)


@overload
def min_not_none(candidates: Iterable[Optional[T]]) -> T:
    return min_not_none(*candidates)


@overload
def min_not_none(*candidates: Optional[T]) -> T:
    return min_not_none(*candidates)


def min_not_none(*candidates: Optional[T]) -> T:
    return _select_not_none(min, *candidates)