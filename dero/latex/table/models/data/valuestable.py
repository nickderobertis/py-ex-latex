from pandas import DataFrame
from dero.latex.table.models.data.row import DataRow


class ValuesTable:

    def __init__(self, rows: [DataRow]):
        self.rows = rows
        self.num_columns = max([len(row) for row in rows])

    @classmethod
    def from_df(cls, df):
        latex_str_list = _build_latex_str_list_from_df(df)
        rows = [DataRow.from_latex_row_str(row_str) for row_str in latex_str_list]
        return cls(rows)

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

