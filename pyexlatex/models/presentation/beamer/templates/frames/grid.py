from typing import Optional, Sequence, Any, List, Tuple
from pyexlatex.models.presentation.beamer.frame.frame import Frame
from pyexlatex.models.presentation.beamer.columns.column import Column
from pyexlatex.models.presentation.beamer.columns.columns import Columns
from pyexlatex.models.layouts.grid import CellLayout, GridLayout


class CellFrame(Frame):
    """
    Lay frame out in a grid where each cell is arbitrarily sized
    """

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
        self.cells = CellLayout(content, grid_shape)

        super().__init__(self.cells.content, **kwargs)


class GridFrame(Frame):
    """
    Creates a CellFrame, automatically setting widths and heights as an even split based on the shape
    of the content passed
    """

    def __init__(self, content: Sequence[Sequence[Any]], **kwargs):
        self.content = content
        self.grid = GridLayout(content)
        super().__init__(self.grid.content, **kwargs)
