from typing import List

import numpy as np

from pyexlatex.table.models.table.section import TableSection
from mixins.repr import ReprMixin


class PanelGrid(ReprMixin):
    repr_cols = ['sections', 'shape']

    def __new__(cls, sections: List[TableSection], shape: tuple=None):
        index_arr = index_array(sections, shape)
        return GridShape.__new__(GridShape, index_arr)


class GridShape(np.ndarray):

    def __new__(cls, input_array, info=None):
        # Input array is an already formed ndarray instance
        # We first cast to be our class type
        obj = np.asarray(input_array).view(cls)
        # add the new attribute to the created instance
        obj.info = info
        # Finally, we must return the newly created object:
        return obj

    def __array_finalize__(self, obj):
        # see InfoArray.__array_finalize__ for comments
        if obj is None: return
        self.info = getattr(obj, 'info', None)

    @property
    def data_has_row_labels(self) -> bool:
        from pyexlatex.table.models.data.table import DataTable
        for section_arr in np.nditer(self, flags=('refs_ok',)):
            section = section_arr.item()
            if isinstance(section, DataTable):
                if section.row_labels is not None and len(section.row_labels.label_collections) > 0:
                    return True
        return False

    @property
    def cell_widths(self) -> List[int]:
        n_cols = self.shape[1]
        widths: List[int] = []
        for row in self:
            width = 0
            for i in range(n_cols):
                section: TableSection = row[i]
                width += section.cell_width
            widths.append(width)
        return widths

    @property
    def cell_width(self) -> int:
        return max(self.cell_widths)


def index_array(sections: List[TableSection], shape: tuple=None):
    if shape is None:
    # default is one column, as many rows as sections
        if sections:
            shape = (len(sections), 1)
        else:
            raise ValueError(f'must pass tuple of shape or sections, got shape: {shape}, sections: {sections}')

    return np.array(sections).reshape(shape)

