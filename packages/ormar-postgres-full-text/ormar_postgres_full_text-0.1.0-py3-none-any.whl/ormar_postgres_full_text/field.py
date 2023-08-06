from typing import Any

import ormar
import sqlalchemy.dialects.postgresql


class TSVector(ormar.fields.model_fields.ModelFieldFactory, str):
    """
    Field factory that creates TSVector Column in the table.
    Beware that the column transforms raw text into TSVector, \
    so after you retrieve model from database, then the field value would be \
    string with set of normalized words.

    e.g.: "hello world hello" -> "'hello' 'world'"
    """

    _type = str
    _sample = "str"

    def __new__(cls, *args: Any, **kwargs: Any) -> ormar.fields.BaseField:
        return super().__new__(cls, *args, **kwargs)

    @classmethod
    def get_column_type(cls, **kwargs) -> sqlalchemy.dialects.postgresql.TSVECTOR:
        return sqlalchemy.dialects.postgresql.TSVECTOR()


def _match(self, other: Any) -> ormar.queryset.clause.FilterGroup:
    """
    Works as 'column @@ to_tsquery(VALUE)'

    Args:
        other: value to check against operator

    Returns:
        FilterGroup for operator.
    """
    return self._select_operator(op="match", other=other)


setattr(ormar.queryset.FieldAccessor, "match", _match)
ormar.queryset.actions.filter_action.FILTER_OPERATORS["match"] = "match"
ormar.queryset.actions.filter_action.METHODS_TO_OPERATORS["match"] = "match"
