import typing

from sqlalchemy import Boolean, Table
from sqlalchemy.sql import ColumnElement
from sqlalchemy.sql.elements import BooleanClauseList


class Filter:
    _mark: str = ''

    def where(self, entity: type | Table):
        pass

    def __bool__(self):
        return False

    @property
    def mark(self):
        return self._mark

    def add_mark(self, mark: str):
        self._mark = mark
        return self


ComparisonOutput = typing.Union[BooleanClauseList, 'ColumnElement[Boolean]']


class Comparison(typing.Protocol):
    def __call__(
        self, attr: ColumnElement, expected: typing.Any
    ) -> ComparisonOutput:
        """Receives column or function and returns a sqlalchemy comparison"""
        ...
