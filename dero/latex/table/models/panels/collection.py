import numpy as np
import pandas as pd

from dero.latex.table.models.panels.panel import Panel
from dero.latex.table.models.panels.panel import PanelGrid
from dero.latex.table.models.labels.table import LabelTable
from dero.latex.models.mixins import ReprMixin
from dero.latex.table.models.table.section import TableSection
from dero.latex.table.logic.panels.combine import common_column_labels, common_row_labels

class PanelCollection(ReprMixin):
    repr_cols = ['name', 'panels']

    def __init__(self, panels: [Panel], label_consolidation: str='object', top_left_corner_labels: LabelTable=None,
                 pad_rows: int=1, pad_columns: int=1, name: str=None):
        """

        :param panels:
        :param label_consolidation: pass 'object' to compare object equality for label consolidation, 'str'
                                    for converting all labels to strings then comparing equality. Use 'object'
                                    for more control over consolidation.
        :param top_left_corner_labels: additional LabelTable of labels to place in the top left corner
        :param pad_rows: horizontal spacing to put between panels
        :param pad_columns: vertical spacing to put between TableSections
        :param name: name that will be used to construct caption in output
        """
        self.name = name
        self.panels = panels
        self.label_consolidation = label_consolidation.lower().strip() \
            if isinstance(label_consolidation, str) else label_consolidation
        self.top_left_corner_labels = top_left_corner_labels \
            if top_left_corner_labels is not None else LabelTable([])
        self.pad_rows = pad_rows
        self.pad_columns = pad_columns

        self.consolidate_labels()

    def iterpanels(self):
        """
        First panel is headers. Then each original panel

        self.grid includes all panels as well as labels. Need to separate back out to
        get each panel
        :return:
        :rtype:
        """

        # grid should have just one extra row of labels
        panel_lengths = [1] + [panel.panel_grid.shape[0] for panel in self.panels]
        assert len(self.grid) == sum(panel_lengths)

        position = 0
        for length in panel_lengths:
            bottom_slice = position
            top_slice = position + length
            yield Panel(self.grid[bottom_slice:top_slice])
            position = position + length

    @property
    def rows(self):
        try:
            return self._rows
        except AttributeError:
            self._rows = self._create_panel_rows()

        return self._rows

    def _create_panel_rows(self):
        column_pad = LabelTable.from_list_of_lists([[' ']]* self.pad_columns)
        rows: [TableSection] = []

        for panel_row in self.grid:
            rows.append(
                panel_row[0] + column_pad.join(panel_row[1:])
            )

        # Now pad rows
        self.num_columns = max([row.num_columns for row in rows])
        for row in rows:
            row.pad(self.num_columns, direction='right')

        return rows


    @property
    def grid(self):
        try:
            return self._grid
        except AttributeError:
            self._grid = np.concatenate([panel.panel_grid for panel in self.panels])

        return self._grid

    def consolidate_labels(self):

        if self.label_consolidation is None:
            return

        if self.label_consolidation == 'object':
            use_object_equality = True
        elif self.label_consolidation in ('string', 'str', True):
            use_object_equality = False
        else:
            raise ValueError(f'must pass object, string, or None to label consolidation. Got {self.label_consolidation}')

        column_labels: [LabelTable] = common_column_labels(
            self.grid,
            use_object_equality=use_object_equality
        )

        row_labels: [LabelTable] = common_row_labels(
            self.grid,
            use_object_equality=use_object_equality
        )

        self._add_column_labels(column_labels)

        # After adding column labels, there is an additional row at the top of the grid
        # Therefore we will need one additional LabelTable for the first row, which is the row of column labels
        # If top_left_corner_labels was passed on object creation, use that as LabelTable. Otherwise use a blank one
        row_labels = [self.top_left_corner_labels] + row_labels
        self._add_row_labels(row_labels)

    def _add_column_labels(self, column_labels: [LabelTable]):
        assert len(column_labels) == self.grid.shape[1]

        # Form PanelGrid from labels
        column_label_grid = PanelGrid(column_labels, shape=(1,len(column_labels)))

        # Combine label PanelGrid and existing PanelGrid
        self._grid = np.concatenate([column_label_grid, self._grid])

    def _add_row_labels(self, row_labels: [LabelTable]):
        assert len(row_labels) == self.grid.shape[0]

        # Form PanelGrid from labels
        row_label_grid = PanelGrid(row_labels, shape=(len(row_labels), 1))

        # Combine label PanelGrid and existing PanelGrid
        self._grid = np.concatenate([row_label_grid, self._grid], axis=1)

    @classmethod
    def from_list_of_lists_of_dfs(cls, df_list_of_lists: [[pd.DataFrame]], *args,
                                  panel_args=tuple(), panel_kwargs={}, **kwargs):
        """
        Note: convenience method for if not much control over table is needed.
        To apply different options to each panel, construct them individually using
        Panel.from_df_list

        :param df_list_of_lists:
        :param args: args to pass to PanelCollection constructor
        :param panel_args: Panel.from_df_list args. Same args will be passed to all panels
        :param panel_kwargs: Panel.from_df_list kwargs. Same kwargs will be passed to all panels
        :param kwargs: kwargs to pass to PanelCollection constructor

        :return: PanelCollection
        """
        panels = []
        for df_list in df_list_of_lists:
            panels.append(
                Panel.from_df_list(df_list, *panel_args, **panel_kwargs)
            )

        return cls(panels, *args, **kwargs)





