
class StringAdditionMixin:

    def __add__(self, other):
        return str(self) + str(other)


class ReprMixin:
    repr_cols = []

    def __repr__(self):
        if self.repr_cols:
            repr_col_strs = [f'{col}={getattr(self, col, None)}' for col in self.repr_cols]
            repr_col_str = f'({", ".join(repr_col_strs)})'
        else:
            repr_col_str = ''
        return f'<{type(self).__name__}{repr_col_str}>'
