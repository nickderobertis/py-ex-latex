from typing import Iterable

class RowAddMixin:

    def __add__(self, other):
        return RowAddMixin.add(self, other)

    def __radd__(self, other):
        return RowAddMixin.radd(self, other)

    def _add_class(self, other):
        from pyexlatex.table.models.table.row import Row
        # keep same class if both are same class
        # otherwise, default to Row class
        self_class = type(self)
        other_class = type(other)
        klass = self_class if self_class == other_class else Row

        return klass

    @staticmethod
    def add(obj, other):
        klass = obj._add_class(other)

        return _add_to_value_or_values(obj, other, klass)

    @staticmethod
    def radd(obj, other):
        klass = obj._add_class(other)

        return _radd_to_value_or_values(obj, other, klass)

def _add_to_value_or_values(obj, other, klass):
    if hasattr(obj, 'value'):
        return _add_to_value(obj, other, klass)
    if hasattr(obj, 'values'):
        return _add_to_values(obj.values, other, klass)
    else:
        raise NotImplementedError

def _radd_to_value_or_values(obj, other, klass):
    if hasattr(obj, 'value'):
        return _radd_to_value(obj, other, klass)
    if hasattr(obj, 'values'):
        return _radd_to_values(obj.values, other, klass)
    else:
        raise NotImplementedError

def _add_to_value(value, other, klass):
    # handle named classes which have value or values attr
    if hasattr(other, 'value'):
        return klass([value, other.value])
    if hasattr(other, 'values'):
        return klass([value] + other.values)

    # handle builtin classes.
    # add lists, tuples, etc
    if isinstance(other, Iterable):
        return klass([value] + list(other))
    # treat as single item, create list out of the two items
    else:
        return klass([value, other])


def _add_to_values(values, other, klass):
    # handle named classes which have value or values attr
    if hasattr(other, 'value'):
        return klass(values + [other.value])
    if hasattr(other, 'values'):
        return klass(values + other.values)

    # handle builtin classes.
    # add lists, tuples, etc
    if isinstance(other, Iterable):
        return klass(values + list(other))
    # treat as single item, append to existing list
    else:
        return klass(values + [other])

def _radd_to_value(value, other, klass):
    # handle builtin classes.
    # add lists, tuples, etc
    if isinstance(other, Iterable):
        return klass(list(other) + [value])
    # treat as single item, create list out of the two items
    else:
        return klass([other, value])


def _radd_to_values(values, other, klass):
    # handle builtin classes.
    # add lists, tuples, etc
    if isinstance(other, Iterable):
        return klass(list(other) + values)
    # treat as single item, append to existing list
    else:
        return klass([other] + values)
