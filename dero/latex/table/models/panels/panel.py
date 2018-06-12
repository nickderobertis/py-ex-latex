import pandas as pd

from dero.latex.table.models.panels.grid import PanelGrid, GridShape
from dero.latex.models.mixins import ReprMixin
from dero.latex.table.models.data.table import DataTable
from dero.latex.table.models.table.row import Row
from dero.latex.table.models.table.section import TableSection



class Panel(ReprMixin):
    repr_cols = ['name', 'panel_grid']

    def __init__(self, panel_grid: PanelGrid, name: str=None):
        self.panel_grid = panel_grid
        self.name = name

    @classmethod
    def from_data_tables(cls, data_table_list: [DataTable], shape: tuple=None, name: str=None):
        """

        :param data_table_list: list of dero.latex.table.DataTable
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
    def from_df_list(cls, df_list: [pd.DataFrame], shape: tuple=None, name: str=None, include_columns=True, include_index=False):
        """

        :param df_list: list of pandas DataFrame
        :param shape: tuple of (rows, columns) to arrange DataFrames. They will be placed from left to right,
                      then from top to bottom.
                      passsing None defaults one column, as many rows as DataFrames
        :param name: name to be displayed with panel
        :param include_columns:
        :param include_index:
        :return:
        """
        data_table_list = [
            DataTable.from_df(
                df,
                include_columns=include_columns,
                include_index=include_index,
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
        rows: [Row] = []
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





