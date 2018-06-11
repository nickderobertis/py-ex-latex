from pandas import DataFrame
from dero.latex.table.models.data.row import DataRow
from dero.latex.table.models.data.dataitem import DataItem
from dero.latex.table.models.table.section import TableSection



class ValuesTable(TableSection):

    def __init__(self, rows: [DataRow]):
        super().__init__(rows)

    @classmethod
    def from_df(cls, df):
        latex_str_list = _build_latex_str_list_from_df(df)
        rows = [DataRow.from_latex_row_str(row_str) for row_str in latex_str_list]
        return cls(rows)

    @classmethod
    def from_list_of_lists(cls, list_of_lists):
        data_rows: [DataRow] = []
        for list_row in list_of_lists:
            data_values = [DataItem(value) for value in list_row]
            data_rows.append(
                DataRow(data_values)
            )

        return cls(data_rows)

    def __add__(self, other):
        # import here to avoid circular imports
        from dero.latex.table.models.spacing.columntable import ColumnPadTable

        table_section: TableSection = super().__add__(other)

        # if just adding padding, retain class rather than drop to general base TableSection
        if isinstance(other, ColumnPadTable):
            return ValuesTable(table_section.rows)
        else:
            return table_section



    def __repr__(self):
        return f'<ValuesTable(shape=({len(self.rows)} , {self.num_columns}))>'


def _build_latex_str_list_from_df(df: DataFrame):
    latex_str = df.to_latex(header=False, index=False)
    latex_list = latex_str.split('\n')

    # for a two row dataframe, latex list will be in the format
    # ['\\begin{tabular}{ll}',
    #  '\\toprule',
    #  ' 03790A & 2011-07-31 \\\\',
    #  ' 03790A & 2011-10-31 \\\\',
    #  '\\bottomrule',
    #  '\\end{tabular}',
    #  '']
    latex_list = latex_list[2:-3] # now contains only data rows

    return latex_list

