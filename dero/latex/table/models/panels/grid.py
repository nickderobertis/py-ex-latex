from dero.latex.table.models.table.section import TableSection
from dero.latex.models.mixins import ReprMixin


class PanelGrid(ReprMixin):
    repr_cols = ['sections', 'shape']

    def __init__(self, sections: [TableSection], shape: tuple=None):
        self.shape = GridShape.from_tuple(shape)
        self.sections = sections


class GridShape(ReprMixin):
    repr_cols = ['rows', 'columns']

    def __init__(self, rows: int, columns: int):
        self.rows = rows
        self.columns = columns

    @classmethod
    def from_tuple(cls, tup, sections: [TableSection]=None):

        if tup is None:
            # default is one column, as many rows as sections
            if sections:
                return cls(len(sections), 1)
            else:
                raise ValueError(f'must pass tuple of shape or sections, got tup: {tup}, sections: {sections}')

        # Handle where a shape tuple is passed
        assert len(tup) == 2
        return cls(tup[0], tup[1])

