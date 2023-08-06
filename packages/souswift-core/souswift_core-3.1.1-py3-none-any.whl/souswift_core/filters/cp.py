import typing
from abc import ABC, abstractmethod

from sqlalchemy import Boolean, Column, func, true
from sqlalchemy.sql.elements import BooleanClauseList
from sqlalchemy.sql.expression import ColumnElement

from souswift_core.filters.base import Comparison, Filter


class Equal(Comparison):
    def __call__(
        self, attr: Column | typing.Any, expected: typing.Any
    ) -> typing.Union[BooleanClauseList, 'ColumnElement[Boolean]']:
        return attr == expected


class NotEqual(Comparison):
    def __call__(
        self, attr: Column | typing.Any, expected: typing.Any
    ) -> typing.Union[BooleanClauseList, 'ColumnElement[Boolean]']:
        return attr != expected


class Greater(Comparison):
    def __call__(
        self, attr: Column | typing.Any, expected: typing.Any
    ) -> typing.Union[BooleanClauseList, 'ColumnElement[Boolean]']:
        return attr > expected


class GreaterEqual(Comparison):
    def __call__(
        self, attr: Column | typing.Any, expected: typing.Any
    ) -> typing.Union[BooleanClauseList, 'ColumnElement[Boolean]']:
        return attr >= expected


class Lesser(Comparison):
    def __call__(
        self, attr: Column | typing.Any, expected: typing.Any
    ) -> typing.Union[BooleanClauseList, 'ColumnElement[Boolean]']:
        return attr < expected


class LesserEqual(Comparison):
    def __call__(
        self, attr: Column | typing.Any, expected: typing.Any
    ) -> typing.Union[BooleanClauseList, 'ColumnElement[Boolean]']:
        return attr <= expected


class Like(Comparison):
    def __call__(
        self, attr: Column | typing.Any, expected: typing.Any
    ) -> typing.Union[BooleanClauseList, 'ColumnElement[Boolean]']:
        return attr.like(f'%{expected}%')


class InsensitiveLike(Comparison):
    def __call__(
        self, attr: Column | typing.Any, expected: typing.Any
    ) -> typing.Union[BooleanClauseList, 'ColumnElement[Boolean]']:
        return attr.ilike(f'%{expected}%')


class Contains(Comparison):
    def __call__(
        self, attr: Column | typing.Any, expected: typing.Any
    ) -> typing.Union[BooleanClauseList, 'ColumnElement[Boolean]']:
        return attr.in_(expected)


class Excludes(Comparison):
    def __call__(
        self, attr: Column | typing.Any, expected: typing.Any
    ) -> typing.Union[BooleanClauseList, 'ColumnElement[Boolean]']:
        return attr.not_in(expected)


class Null(Comparison):
    def __call__(
        self, attr: Column | typing.Any, isnull: bool
    ) -> typing.Union[BooleanClauseList, 'ColumnElement[Boolean]']:
        return attr.is_(None) if isnull else attr.is_not(None)


class JSONContains(Comparison):
    def __call__(
        self, attr: Column | typing.Any, expected: typing.Any
    ) -> typing.Union[BooleanClauseList, 'ColumnElement[Boolean]']:
        return func.json_contains(attr, f'"{expected}"')  # type: ignore


class EmptyJson(Comparison):
    def __call__(
        self, attr: Column | typing.Any, expected: typing.Any
    ) -> typing.Union[BooleanClauseList, 'ColumnElement[Boolean]']:
        return func.json_length(attr) == 0


class RelatedComp(ABC):
    def __init__(self, where: Filter):
        self._where = where

    def __bool__(self):
        return self._where.__bool__()

    @abstractmethod
    def __call__(
        self, attr: type, expected: Column | typing.Any
    ) -> typing.Union[BooleanClauseList, 'ColumnElement[Boolean]']:
        ...


class RelatedWhere(RelatedComp):
    def __call__(
        self, attr: type, expected: Column | typing.Any
    ) -> typing.Union[BooleanClauseList, 'ColumnElement[Boolean]']:
        return self._where.where(attr)


class RelatedHas(RelatedComp):
    def __call__(
        self, attr: type, expected: Column | typing.Any
    ) -> typing.Union[BooleanClauseList, 'ColumnElement[Boolean]']:
        return attr.has(self._where.where(attr))


class RelatedAny(RelatedComp):
    def __call__(
        self, attr: type, expected: Column | typing.Any
    ) -> typing.Union[BooleanClauseList, 'ColumnElement[Boolean]']:
        return attr.any(self._where.where(attr))


class RelatedEmpty(RelatedComp):
    def __call__(
        self, attr: type, expected: Column | typing.Any
    ) -> typing.Union[BooleanClauseList, 'ColumnElement[Boolean]']:
        return ~expected.any()


class AlwaysTrue(Comparison):
    """Just an empty Comparison, or a comparison placeholder"""

    def __call__(
        self, *__args, **__kwargs
    ) -> typing.Union[BooleanClauseList, 'ColumnElement[Boolean]']:
        return true()
