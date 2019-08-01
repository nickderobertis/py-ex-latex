from typing import Optional, Sequence, Any, List
from dero.latex.models.presentation.beamer.frame.frame import Frame
from dero.latex.models.presentation.beamer.columns.column import Column
from dero.latex.models.presentation.beamer.columns.columns import Columns


class GridFrame(Frame):

    def __init__(self, content: Sequence[Sequence[Any]], grid_shape: Sequence[Sequence[float]], **kwargs):
        self.content = content
        self.grid_shape = grid_shape
        self._validate()

        super().__init__(self.column_content, **kwargs)

    def _validate(self):
        value_error = ValueError(f'must pass content and grid_shape of the same dimensions, '
                                 f'got content {self.content} and grid_shape {self.grid_shape}')
        if len(self.content) != len(self.grid_shape):
            raise value_error

        for i, content_row in enumerate(self.content):
            shape_row = self.grid_shape[i]
            if len(shape_row) != len(content_row):
                raise value_error

    @property
    def column_content(self) -> List[Columns]:
        content_in_columns = []
        for row_num, shape_row in enumerate(self.grid_shape):
            cells = []
            for col_num, width in enumerate(shape_row):
                cell_content = self.content[row_num][col_num]
                cell = Column(cell_content, frac_of_text_width=width)
                cells.append(cell)
            row = Columns(cells)
            content_in_columns.append(row)

        return content_in_columns
