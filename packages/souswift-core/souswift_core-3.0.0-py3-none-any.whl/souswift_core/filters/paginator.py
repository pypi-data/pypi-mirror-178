import typing

from sqlalchemy.sql import Select

from souswift_core.filters import comp, where


class Paginate(typing.Protocol):
    def __call__(self, query: Select) -> Select:
        ...


def limit_offset_paginate(limit: int, page: int) -> Paginate:
    def paginate(query: Select) -> Select:
        return query.limit(limit).offset(page * limit)

    return paginate


def id_paginate(limit: int, last_id: int) -> Paginate:
    def paginate(query: Select) -> Select:
        return query.where(
            where.Field('pk', last_id, comp=comp.greater).where(
                query.selected_columns
            )
        ).limit(limit)

    return paginate


def _null_paginate(limit: int, offset: int) -> Paginate:
    del limit, offset

    def paginate(query: Select) -> Select:
        return query

    return paginate


null_paginate = _null_paginate(0, 0)
