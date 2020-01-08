from typing import List

import pandas as pd

from pyexlatex.logic.tools import _max_len_or_zero
from pyexlatex.table.models.panels.grid import PanelGrid, GridShape
from mixins.repr import ReprMixin
from pyexlatex.table.models.data.table import DataTable
from pyexlatex.table.models.table.row import Row
from pyexlatex.table.models.table.section import TableSection



class Panel(ReprMixin):
    """
    Represents one section of a table. May have multiple DataTables within one panel.


    """
    repr_cols = ['name', 'panel_grid']

    def __init__(self, panel_grid: PanelGrid, name: str=None):
        self.panel_grid = panel_grid
        self.name = name

    @classmethod
    def from_data_tables(cls, data_table_list: List[DataTable], shape: tuple=None, name: str=None):
        """

        :param data_table_list: list of pyexlatex.table.DataTable
        :param shape: tuple of (rows, columns) to arrange DataTables. They will be placed from left to right,
                      then from top to bottom.
                      passsing None defaults one column, as many rows as DataTables
        :param name: name to be displayed with panel
        :return:
        """
        return cls(PanelGrid(data_table_list, shape=shape), name=name)

    @classmethod
    def from_df(cls, df: pd.DataFrame, include_columns=True, include_index=False, name: str=None):
        data_table = DataTable.from_df(
            df,
            include_columns=include_columns,
            include_index=include_index
        )

        return cls.from_data_tables([data_table], name=name)

    @classmethod
    def from_df_list(cls, df_list: List[pd.DataFrame], shape: tuple=None, name: str=None, include_columns=True,
                     include_index=False, data_table_kwargs={}):
        """

        :param df_list: list of pandas DataFrame
        :param shape: tuple of (rows, columns) to arrange DataFrames. They will be placed from left to right,
                      then from top to bottom.
                      passsing None defaults one column, as many rows as DataFrames
        :param name: name to be displayed with panel
        :param include_columns:
        :param include_index:
        :param data_table_kwargs: kwargs to be passed to DataTable.from_df. Same kwargs will be passed to
                                  all data tables.
        :return:
        """
        data_table_list = [
            DataTable.from_df(
                df,
                include_columns=include_columns,
                include_index=include_index,
                **data_table_kwargs
            )
            for df in df_list
        ]

        return cls.from_data_tables(data_table_list, shape=shape, name=name)

    @property
    def rows(self):
        try:
            return self._rows
        except AttributeError:
            self._rows = self._set_rows()

        return self._rows

    def _set_rows(self):
        from pyexlatex.table.models.labels.table import LabelTable, LabelCollection
        from pyexlatex.table.models.labels.label import Label
        rows: [Row] = []

        # Add panel name
        if self.name is not None:
            label_collection = LabelCollection([Label(self.name, span=self.num_columns, align='l')])
            name_table = LabelTable([label_collection])
            rows += name_table.rows

        for grid_row in self.panel_grid:
            for i, table_section in enumerate(grid_row):
                if i == 0:
                    panel_row = table_section
                else:
                    panel_row += table_section
            rows += panel_row.rows
        return rows

    @property
    def is_spacer(self):
        return all([row.is_spacer for row in self.rows])

    @property
    def num_columns(self):
        num_columns = 0
        for grid_row in self.panel_grid:
            row_num_columns = [table_section.num_columns for table_section in grid_row]
            max_for_row = max(row_num_columns)
            num_columns = max(num_columns, max_for_row) # update global max with row max
        return num_columns






