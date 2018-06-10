from dero.latex.logic.tools import show_contents

class StringAdditionMixin:

    def __add__(self, other):
        return str(self) + str(other)

    def __radd__(self, other):
        return str(other) + str(self)

    def join(self, iterable):
        return self.__str__().join(str(i) for i in iterable)


class ReprMixin:
    repr_cols = []

    def __repr__(self):
        if self.repr_cols:
            repr_col_strs = [f'{col}={getattr(self, col, None).__repr__()}' for col in self.repr_cols]
            repr_col_str = f'({", ".join(repr_col_strs)})'
        else:
            repr_col_str = ''
        return f'<{type(self).__name__}{repr_col_str}>'

    @property
    def readable_repr(self):
        return show_contents(self)