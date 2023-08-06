import typing
from datetime import date, time

import sqlalchemy as sa
from sqlalchemy.sql import ColumnElement

from . import base

SortableTypeDef: typing.TypeAlias = int | float | date | time

SequenceTypeDef: typing.TypeAlias = list | tuple


def equals(attr: ColumnElement, expected: typing.Any) -> base.ComparisonOutput:
    return attr == expected


def not_equals(
    attr: ColumnElement, expected: typing.Any
) -> base.ComparisonOutput:
    return attr != expected


def greater(
    attr: ColumnElement, expected: SortableTypeDef
) -> base.ComparisonOutput:
    return attr > expected


def greater_equals(
    attr: ColumnElement, expected: SortableTypeDef
) -> base.ComparisonOutput:
    return attr >= expected


def lesser(
    attr: ColumnElement, expected: SortableTypeDef
) -> base.ComparisonOutput:
    return attr < expected


def lesser_equals(
    attr: ColumnElement, expected: SortableTypeDef
) -> base.ComparisonOutput:
    return attr <= expected


def between(
    attr: ColumnElement,
    expected: tuple[SortableTypeDef, SortableTypeDef],
) -> base.ComparisonOutput:
    left, right = expected
    return attr.between(left, right)


def like(attr: ColumnElement, expected: str) -> base.ComparisonOutput:
    return attr.like(f'%{expected}%')


def ilike(attr: ColumnElement, expected: str) -> base.ComparisonOutput:
    return attr.ilike(f'%{expected}%')


def contains(
    attr: ColumnElement, expected: SequenceTypeDef
) -> base.ComparisonOutput:
    return attr.in_(expected)


def excludes(
    attr: ColumnElement, expected: SequenceTypeDef
) -> base.ComparisonOutput:
    return attr.not_in(expected)


def isnull(attr: ColumnElement, expected: bool) -> base.ComparisonOutput:
    return attr.is_(None) if expected else attr.is_not(expected)


def always_true(
    attr: ColumnElement, expected: typing.Any
) -> base.ComparisonOutput:
    del attr, expected
    return sa.true()
