from typing import Optional, Sequence, Any, List, Tuple
from dero.latex.models.presentation.beamer.frame.frame import Frame
from dero.latex.models.presentation.beamer.columns.column import Column
from dero.latex.models.presentation.beamer.columns.columns import Columns


class GridFrame(Frame):

    def __init__(self, content: Sequence[Sequence[Any]], grid_shape: Sequence[Sequence[Tuple[float, float]]], **kwargs):
        """

        Args:
            content:
            grid_shape: list of list of tuples of (width, height), e.g. [
                    [(0.3, 0.4), (0.7, 0.4)],
                    [(0.3, 0.6), (0.7, 0.6)],
                ] would create a 2x2 grid with 40% of height in the first row, 60% in the second row. 30% width in the
                first column, 70% width in the second column.
            **kwargs:
        """
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
            for col_num, (width, height) in enumerate(shape_row):
                cell_content = self.content[row_num][col_num]
                cell = Column(
                    cell_content,
                    frac_of_text_width=self._rescale_width(width, len(shape_row)),
                    frac_of_page_height=self._rescale_height(height)
                )
                cells.append(cell)
            row = Columns(cells)
            content_in_columns.append(row)

        return content_in_columns

    @staticmethod
    def _rescale_height(height: float):
        """
        With the standard Madrid header and footer, 0.8\textheight is about the full area with a bit of padding on
        top and bottom. Therefore passing 0.5 should be rescaled to 50% of the available area, or 0.4\textheight
        """
        # TODO: think about other themes having different text area
        available_area = 0.8
        return height * available_area

    @staticmethod
    def _rescale_width(width: float, num_cols: int):
        """
        Latex adds padding inbetween the columns, so 100% area is not really available. Need to set the available
        area based on the number of columns
        Args:
            width:
            num_cols:

        Returns:
        """
        # TODO: figure out how available area changes based on number of columns. Defaulting to doing nothing now
        available_area = 1
        return width * available_area


class AutoSizeGridFrame(GridFrame):
    """
    Creates a GridFrame, automatically setting widths and heights as an even split based on the shape
    of the content passed
    """

    def __init__(self, content: Sequence[Sequence[Any]], **kwargs):
        grid_shape = []
        num_rows = len(content)
        height = 1/num_rows
        for row in content:
            num_columns = len(row)
            width = 1/num_columns
            grid_shape.append([(width, height) for _ in range(len(row))])
        super().__init__(content, grid_shape, **kwargs)
