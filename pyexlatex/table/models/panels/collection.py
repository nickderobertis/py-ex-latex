from copy import deepcopy
from typing import Union, AnyStr, List, Optional

import numpy as np
import pandas as pd

from mixins.repr import ReprMixin

from pyexlatex.table.logic.panels.combine import (
    common_column_labels,
    common_row_labels,
    remove_label_collections_from_grid
)
from pyexlatex.table.logic.panels.letters import panel_string
from pyexlatex.table.logic.panels.topleft import _set_top_left_corner_labels
from pyexlatex.table.models.labels.table import LabelTable, LabelCollection
from pyexlatex.table.models.panels.panel import Panel
from pyexlatex.table.models.panels.panel import PanelGrid, GridShape
from pyexlatex.table.models.spacing.columntable import ColumnPadTable
from pyexlatex.table.models.spacing.rowtable import RowPadTable
from pyexlatex.table.models.table.section import TableSection
from pyexlatex.table.models.data.table import DataTable


class PanelCollection(ReprMixin):
    """
    Lays panel contents in a grid, consolidates labels, creates padding between tables

    """
    repr_cols = ['name', 'panels']
    _num_columns: int

    def __init__(self, panels: List[Panel], label_consolidation: str='object', enforce_label_order=True,
                 top_left_corner_labels: Union[LabelTable, LabelCollection, List[AnyStr], AnyStr]=None,
                 pad_rows: int=1, pad_columns: int=1, name: str=None):
        """

        :param panels: list of Panels, which represent a full set of rows of the table. for multiple
                        sections in one set of rows, create DataTables for each section and pass to Panels.
        :param label_consolidation: pass 'object' to compare object equality for label consolidation, 'str'
                                    for converting all labels to strings then comparing equality. Use 'object'
                                    for more control over consolidation.
        :param enforce_label_order: pass False to allow consolidating lower labels even if upper labels do not match.
                                    e.g. if labels on one table are [['Top1'], ['Bot1', 'Bot2']], then labels on the other
                                    table are [['Top2'], ['Bot1', 'Bot2']], consolidated labels when passing False will be
                                    ['Bot1', 'Bot2'], while when passing True, no labels will be consolidated. Under True,
                                    will start from the top label, then stop consolidating once it has a mismatch.
        :param top_left_corner_labels: additional labels to place in the top left corner. pass a single string
                                       or a list of strings for convenience. a list of strings will be create labels
                                       which span the gap horizontally and go downwards, one label per row. pass
                                       LabelCollection or LabelTable for more control.
        :param pad_rows: horizontal spacing to put between panels
        :param pad_columns: vertical spacing to put between TableSections
        :param name: name that will be used to construct caption in output
        """
        self.name = name
        self.panels = panels
        self.label_consolidation = label_consolidation.lower().strip() \
            if isinstance(label_consolidation, str) else label_consolidation
        self.enforce_label_order = enforce_label_order
        self.top_left_corner_labels = _set_top_left_corner_labels(top_left_corner_labels)
        self.pad_rows = pad_rows
        self.pad_columns = pad_columns

        self.has_row_labels = False
        self.has_column_labels = False

        self.consolidate_labels()
        self.pad_grid()

    def iterpanels(self, add_panel_order_label: bool = True):
        """
        First panel is headers. Then each original panel

        self.grid includes all panels as well as labels. Need to separate back out to
        get each panel

        :param add_panel_order_label: Whether to add to names of panels Panel A:, Panel B:,
        and so on

        :return:
        :rtype:
        """

        # Get lengths of panels
        if len(self.panels) > 1:
            # Include spacing which is added in pad_grid
            panel_lengths = [panel.panel_grid.shape[0] * 2 - 1 for panel in self.panels]
        else:
            panel_lengths = [self.panels[0].panel_grid.shape[0]]
        if self.has_column_labels:
            # First panel will have an additional row at the top if there are column labels
            panel_lengths[0] += 1

        total_row_idx = 0
        for panel_idx, panel_length in enumerate(panel_lengths):
            for row_idx in range(panel_length):
                row = self.rows[total_row_idx]
                # if first part of actual panel, below labels, and panel has a name
                if (
                        (
                            # If it's the first panel, and there's column labels, then second row should show name
                            self.has_column_labels and panel_idx == 0 and row_idx == 1 or
                            # If it's a later panel, or there's no column labels, first row should show name
                            (not self.has_column_labels or panel_idx > 0) and row_idx == 0
                        ) and
                        # Has to have name to show name
                        self.panels[panel_idx].name is not None
                ):
                    # output with the name
                    if add_panel_order_label:
                        full_name = panel_string(panel_idx) + self.panels[panel_idx].name
                    else:
                        full_name = self.panels[panel_idx].name
                    yield Panel(PanelGrid([row]), name=full_name)
                else:
                    # column labels panel, no matching name. Or no name for user supplied panel
                    yield Panel(PanelGrid([row]))
                total_row_idx += 1
            # If we are in-between panels, not on the last panel
            if panel_idx + 1 != len(self.panels) and self.pad_rows > 0:
                for _ in range(self.pad_rows):
                    # In between panels, there are also spacers, yield those
                    row = self.rows[total_row_idx]
                    yield Panel(PanelGrid([row]))
                    total_row_idx += 1

    @property
    def rows(self):
        try:
            return self._rows
        except AttributeError:
            self._rows = self._create_panel_rows()

        return self._rows

    @property
    def num_columns(self) -> int:
        try:
            return self._num_columns
        except AttributeError:
            self._num_columns = max([row.num_columns for row in self.rows])

        return self._num_columns

    def _create_panel_rows(self):
        rows: [TableSection] = []
        for panel_row in self.grid:
            new_row = None
            for i, section in enumerate(panel_row):
                if i == 0:
                    new_row = section
                else:
                    new_row = new_row + section
            if new_row:
                rows.append(new_row)

        try:
            num_columns = self._num_columns
        except AttributeError:
            num_columns = max([row.num_columns for row in rows])
        # Now pad rows
        for row in rows:
            row.pad(num_columns, direction='right')


        return rows


    @property
    def grid(self):
        try:
            return self._grid
        except AttributeError:
            self._grid = _concatenate_uneven_rows_filling_right(
                [panel.panel_grid for panel in self.panels],
                fill_value=TableSection([]),
                array_class=GridShape
            )

        return self._grid

    def consolidate_labels(self):

        # TODO [#46]: reduce complexity and improve testing of label consolidation
        #
        # This code has grown quite a bit to handle all the cases, and it
        # still has not been thoroughly tested for every case. Need to expand
        # the testing to cover all the cases and then try to simplify the code

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
            use_object_equality=use_object_equality,
            enforce_label_order=self.enforce_label_order
        )
        # Column labels may be modified to add top left corner label, but need to
        # track original so it can be removed from existing panels
        orig_column_labels = deepcopy(column_labels)

        row_labels: [LabelTable] = common_row_labels(
            self.grid,
            use_object_equality=use_object_equality,
            enforce_label_order=self.enforce_label_order
        )

        # Remove from the original tables the labels that were just consolidated
        remove_label_collections_from_grid(
            self.grid,
            column_labels=orig_column_labels,
            row_labels=row_labels,
            use_object_equality=use_object_equality
        )

        if column_labels is not None:
            if row_labels is None and not self.top_left_corner_labels.is_spacer:
                # If there are column labels but not row labels, still need to deal with top left label.
                # Adding the top left label is handled in the if row_labels is not None block, but it will
                # not be reached as row_labels is None. Therefore create a blank label table for each grid row
                # except for the column labels. The top left label to go with the column row will be added
                # in the following block.
                # Grid shape -1 to exclude just added column labels
                row_labels: List[LabelTable] = []
                for grid_row in self.grid:
                    left_value: TableSection = grid_row[0]
                    if left_value in column_labels:
                        # top left corner label, handled separately in row labels section
                        continue
                    section_height = len(left_value.rows)
                    if isinstance(left_value, DataTable):
                        if left_value.column_labels in column_labels:
                            # Adjust for when the column labels have been consolidated into the overall column labels,
                            # then don't need to add row label as this column label won't be in the output
                            section_height -= 1
                    label_lol = [['']] * section_height
                    row_labels.append(LabelTable.from_list_of_lists(label_lol))

        column_labels_created = False
        if row_labels is not None:
            if column_labels is not None:
                self._add_column_labels(column_labels)
                column_labels_created = True
            # After adding column labels, there is an additional row at the top of the grid
            # Therefore we will need one additional LabelTable for the first row, which is the row of column labels
            # If top_left_corner_labels was passed on object creation, use that as LabelTable. Otherwise use a blank one
            if self.has_column_labels:
                all_row_labels = [self.top_left_corner_labels] + row_labels
            else:
                all_row_labels = row_labels
            self._add_row_labels(all_row_labels)
        elif column_labels is not None:
            # There are no common row labels, but if there are any row labels which are not being consolidated,
            # still need to add the top left corner
            # First detect the existence of any row labels
            any_row_labels = False
            for grid_row in self.grid:
                left_value: TableSection = grid_row[0]
                if isinstance(left_value, DataTable) and left_value.has_row_labels:
                    any_row_labels = True
            if any_row_labels:
                # Now add the top left corner
                column_labels[0] = self.top_left_corner_labels + column_labels[0]

        if column_labels is not None and not column_labels_created:
            self._add_column_labels(column_labels)


    def pad_grid(self):
        row_pad = RowPadTable()

        grid_rows: [GridShape] = []
        for n_row, grid_row in enumerate(self.grid):
            # Add first elem
            new_row = np.array([grid_row[0]]).view(GridShape).reshape(1,1)
            # Add following elems
            for n_elem, elem in enumerate(grid_row[1:]):
                # Add pads between following elems
                if self.pad_columns and not (n_elem == 0 and self.has_row_labels): # only skip first if there are row labels
                    new_row = np.append(new_row, np.array([ColumnPadTable(self.pad_columns)])).view(GridShape)
                new_row = np.append(new_row, elem).view(GridShape)
                new_row = new_row.reshape((1, new_row.shape[0])) # reorganize into row
            grid_rows.append(new_row)
            # add row padding on every loop except last
            if n_row != self.grid.shape[0] - 1:
                # no need to add padding after column labels
                if n_row == 0 and self.has_column_labels:
                    continue
                for i in range(self.pad_rows):
                    grid_rows.append(
                        np.array([row_pad]).view(GridShape).reshape(1,1)
                    )

        # Before combining rows, must have same number of elements. Pad right with empty label tables
        num_grid_columns = max(row.shape[1] for row in grid_rows) # find max number of columns
        out_grid_rows = []
        for row in grid_rows:
            pad_number = num_grid_columns - row.shape[1]
            assert pad_number >= 0
            new_row = np.append(row, np.array([row_pad] * pad_number)).view(GridShape)
            new_row = new_row.reshape((1, new_row.shape[0]))  # reorganize into row
            out_grid_rows.append(new_row)

        new_grid = np.concatenate(out_grid_rows).view(GridShape)
        self._grid = new_grid
        self._rows = self._create_panel_rows() # need to recreate rows with new grid

    def _add_column_labels(self, column_labels: List[LabelTable]):
        assert len(column_labels) == self.grid.shape[1]

        if all(table.is_empty for table in column_labels):
            # if no consolidated labels, no need to add
            self.has_column_labels = False
            return

        self.has_column_labels = True

        # Form PanelGrid from labels
        column_label_grid = PanelGrid(column_labels, shape=(1,len(column_labels)))

        # Combine label PanelGrid and existing PanelGrid
        self._grid = np.concatenate([column_label_grid, self._grid]).view(GridShape)

    def _add_row_labels(self, row_labels: List[LabelTable]):
        assert len(row_labels) == self.grid.shape[0]

        if all(table.is_empty for table in row_labels):
            # if no consolidated labels, no need to add
            self.has_row_labels = False
            return

        self.has_row_labels = True

        # Form PanelGrid from labels
        row_label_grid = PanelGrid(row_labels, shape=(len(row_labels), 1))

        # Combine label PanelGrid and existing PanelGrid
        self._grid = np.concatenate([row_label_grid, self._grid], axis=1).view(GridShape)

    @classmethod
    def from_list_of_lists_of_dfs(cls, df_list_of_lists: List[List[pd.DataFrame]],
                                  panel_names: List[str] = None, *args,
                                  panel_kwargs={},
                                  data_table_kwargs={}, **kwargs):
        """
        To create a single panel table, pass a single list within
        a list of DataFrames, e.g. [[df1, df2]] then shape will specify how the DataFrames will
        be organized in the Panel. If you pass two lists within the outer list, then shape will
        apply to each Panel. So [[df1, df2], [df3, df4]] with shape=(1,2) create a two Panel table
        with two tables placed within each panel going horizontally, so that the overall shape is (2,2).

        Note: convenience method for if not much control over table is needed.
        To apply different options to each panel, construct them individually using
        Panel.from_df_list

        :param df_list_of_lists:
        :param panel_names: list of panel names. Must be of same length as outer list in df_list_of_lists
        :param args: args to pass to PanelCollection constructor
        :param panel_kwargs: Panel.from_df_list kwargs. Same kwargs will be passed to all panels
        :param kwargs: kwargs to pass to PanelCollection constructor
        :param data_table_kwargs: kwargs to be passed to DataTable.from_df. Same kwargs will be passed to
                                  all data tables.

        :return: PanelCollection
        """
        _validate_panel_names(panel_names, df_list_of_lists)

        panels = []
        for i, df_list in enumerate(df_list_of_lists):
            panel_name = _panel_name_or_none(panel_names, i)
            panels.append(
                Panel.from_df_list(
                    df_list,
                    name=panel_name,
                    data_table_kwargs=data_table_kwargs,
                    **panel_kwargs)
            )

        label_consolidation = kwargs.pop('label_consolidation', 'string')

        return cls(
            panels,
            label_consolidation=label_consolidation,
            **kwargs
        )

    def to_tex(self, mid_rule=True):
        from pyexlatex.table.logic.table.build import build_tabular_content_from_panel_collection
        return build_tabular_content_from_panel_collection(self, mid_rule=mid_rule)

def _panel_name_or_none(panel_names: Optional[List[str]], index: int):
    if panel_names is not None:
        return panel_names[index]
    else:
        return None

def _validate_panel_names(panel_names: Optional[List[str]], df_list_of_lists: List[List[pd.DataFrame]]):
    if panel_names is None:
        return

    num_panel_names = len(panel_names)
    num_panels = len(df_list_of_lists)
    if num_panel_names != num_panels:
        raise ValueError(f'must pass as many panel names as panels. Got {num_panel_names} names '
                         f'and {num_panels} panels.')


def _concatenate_uneven_rows_filling_right(rows, fill_value=np.nan, array_class=None):
    """
    Concatenates along vertical axis, filling right as needed.

    Examples:
        a = np.array(
            [[1, 2, 3]]
        )
        b = np.array(
            [[4, 5]]
        )
        _concatenate_uneven_rows_filling_right([a, b])

        array([[ 1.,  2.,  3.],
               [ 4.,  5., nan]])

    Args:
        rows:
        fill_value:
        array_class:

    Returns:

    """
    max_len = max([row.shape[1] for row in rows])

    concat_rows = []
    for row in rows:
        num_to_add = max_len - row.shape[1]
        if num_to_add > 0:
            add_array = np.array([[fill_value] * num_to_add])
            concat_array = np.concatenate([row, add_array], axis=1)
        else:
            concat_array = row
        concat_rows.append(concat_array)

    out_arr = np.concatenate(concat_rows)

    if array_class:
        out_arr = out_arr.view(array_class)

    return out_arr