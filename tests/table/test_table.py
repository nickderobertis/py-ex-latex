from copy import deepcopy

import pandas as pd

import pyexlatex as pl
from tests.base import GENERATED_FILES_DIR
from tests.utils.pdf import compare_pdfs_in_generated_vs_input_by_name

EXAMPLE_DF = pd.DataFrame(
    [
        (1, 2, 3),
        (4, 5, 6),
        (7, 8, 9)
    ],
    columns=['a', 'b', 'c']
)
EXAMPLE_DF_WITH_NAMED_INDEX = deepcopy(EXAMPLE_DF)
EXAMPLE_DF_WITH_NAMED_INDEX.index.name = 'index_name'
EXAMPLE_DF_WITH_DECIMALS = pd.DataFrame(
    [
        (1, 2.54, 3.1),
        (4, 50, 654),
        (7, 8.114, 9.541)
    ],
    columns=['a', 'b', 'c']
)

class TestTable:
    table = pl.Table.from_list_of_lists_of_dfs(
        [[EXAMPLE_DF]],
        caption='My Table Title',
        below_text='My below text',
        mid_rules=False,
    )
    two_panel_table_from_dict_no_index = pl.Table.from_panel_name_df_dict(
        {
            'One': EXAMPLE_DF,
            'Two': (EXAMPLE_DF + 10)
        },
        caption='My Table Title',
        below_text='My below text'
    )
    two_panel_table_from_lol_no_index = pl.Table.from_list_of_lists_of_dfs(
        [[EXAMPLE_DF], [EXAMPLE_DF + 10]],
        panel_names=['One', 'Two'],
        caption='My Table Title',
        below_text='My below text'
    )
    two_panel_table_from_dict_no_index_with_tl = pl.Table.from_panel_name_df_dict(
        {
            'One': EXAMPLE_DF,
            'Two': (EXAMPLE_DF + 10)
        },
        caption='My Table Title',
        below_text='My below text',
        top_left_corner_labels='woo'
    )
    two_panel_table_from_lol_no_index_with_tl = pl.Table.from_list_of_lists_of_dfs(
        [[EXAMPLE_DF], [EXAMPLE_DF + 10]],
        panel_names=['One', 'Two'],
        caption='My Table Title',
        below_text='My below text',
        top_left_corner_labels=['woo'],
    )
    two_panel_table_from_dict_with_index = pl.Table.from_panel_name_df_dict(
        {
            'One': EXAMPLE_DF,
            'Two': (EXAMPLE_DF + 10)
        },
        caption='My Table Title',
        below_text='My below text',
        include_index=True
    )
    two_panel_table_from_dict_with_index_and_name = pl.Table.from_panel_name_df_dict(
        {
            'One': EXAMPLE_DF_WITH_NAMED_INDEX,
            'Two': (EXAMPLE_DF_WITH_NAMED_INDEX + 10)
        },
        caption='My Table Title',
        below_text='My below text',
        include_index=True,
        align = 'lccc',
    )
    two_panel_table_from_dict_with_index_and_tl = pl.Table.from_panel_name_df_dict(
        {
            'One': EXAMPLE_DF,
            'Two': (EXAMPLE_DF + 10)
        },
        caption='My Table Title',
        below_text='My below text',
        include_index=True,
        top_left_corner_labels='TL Label'
    )
    two_panel_table_from_lol_with_index = pl.Table.from_list_of_lists_of_dfs(
        [[EXAMPLE_DF], [EXAMPLE_DF + 10]],
        panel_names=['One', 'Two'],
        caption='My Table Title',
        below_text='My below text',
        include_index=True
    )
    two_panel_table_from_lol_with_index_and_name = pl.Table.from_list_of_lists_of_dfs(
        [[EXAMPLE_DF_WITH_NAMED_INDEX], [EXAMPLE_DF_WITH_NAMED_INDEX + 10]],
        panel_names=['One', 'Two'],
        caption='My Table Title',
        below_text='My below text',
        include_index=True,
    )
    two_panel_table_from_lol_with_index_and_tl = pl.Table.from_list_of_lists_of_dfs(
        [[EXAMPLE_DF], [EXAMPLE_DF + 10]],
        panel_names=['One', 'Two'],
        caption='My Table Title',
        below_text='My below text',
        include_index=True,
        top_left_corner_labels='TL Label'
    )
    two_panel_table_from_dict_no_pad = pl.Table.from_panel_name_df_dict(
        {
            'One': EXAMPLE_DF,
            'Two': (EXAMPLE_DF + 10)
        },
        caption='My Table Title',
        below_text='My below text',
        include_index=True,
        pad_rows=0,
    )
    two_panel_table_from_dict_double_pad = pl.Table.from_panel_name_df_dict(
        {
            'One': EXAMPLE_DF,
            'Two': (EXAMPLE_DF + 10)
        },
        caption='My Table Title',
        below_text='My below text',
        include_index=True,
        pad_rows=2,
    )
    two_panel_table_from_lol_no_pad = pl.Table.from_list_of_lists_of_dfs(
        [[EXAMPLE_DF], [EXAMPLE_DF + 10]],
        panel_names=['One', 'Two'],
        caption='My Table Title',
        below_text='My below text',
        include_index=True,
        pad_rows=0,
        pad_columns=0,
    )
    two_panel_table_from_lol_double_pad = pl.Table.from_list_of_lists_of_dfs(
        [[EXAMPLE_DF], [EXAMPLE_DF + 10]],
        panel_names=['One', 'Two'],
        caption='My Table Title',
        below_text='My below text',
        include_index=True,
        pad_rows=2,
        pad_columns=0,
    )
    table_from_lol_with_short_caption = pl.Table.from_list_of_lists_of_dfs(
        [[EXAMPLE_DF]],
        caption='My Table Title',
        short_caption='Short Capt',
        below_text='My below text',
        mid_rules=False,
    )
    table_from_dict_with_short_caption = pl.Table.from_panel_name_df_dict(
        {
            'One': EXAMPLE_DF,
        },
        caption='My Table Title',
        short_caption='Short Capt',
        below_text='My below text',
        mid_rules=False,
    )
    table_with_siunitx_aligns = pl.Table.from_list_of_lists_of_dfs(
        [[EXAMPLE_DF_WITH_DECIMALS]],
        caption='My Table Title',
        below_text='My below text',
        mid_rules=False,
        align='lS[table-column-width=4cm]s'
    )
    table_with_dcolumn_aligns = pl.Table.from_list_of_lists_of_dfs(
        [[EXAMPLE_DF_WITH_DECIMALS]],
        caption='My Table Title',
        below_text='My below text',
        mid_rules=False,
        align='ld{2.3}D{.}{,}{3.3}'
    )
    table_with_spacing_adjust_aligns = pl.Table.from_list_of_lists_of_dfs(
        [[EXAMPLE_DF_WITH_DECIMALS]],
        caption='My Table Title',
        below_text='My below text',
        mid_rules=False,
        align='@{}l!{}c@{}c@{}'
    )
    table_with_position_str = pl.Table.from_list_of_lists_of_dfs(
        [[EXAMPLE_DF]],
        caption='My Table Title',
        below_text='My below text',
        mid_rules=False,
        position_str='htb'
    )
    table_with_tl = pl.Table.from_list_of_lists_of_dfs(
        [[EXAMPLE_DF]],
        caption='My Table Title',
        top_left_corner_labels='TL Header',
    )
    data_table_with_index_and_tl = pl.DataTable.from_df(
        EXAMPLE_DF,
        include_index=True,
        top_left_corner_labels='TL Header'
    )
    panel_with_index_and_tl = pl.Panel.from_data_tables([data_table_with_index_and_tl])
    table_from_panel_with_index_and_tl = pl.Table.from_panel_list([panel_with_index_and_tl])
    data_table_with_index_and_all_headers = pl.DataTable.from_df(
        EXAMPLE_DF,
        include_index=True,
        extra_header='Header',
        top_left_corner_labels='TL Header'
    )
    panel_with_index_and_all_headers = pl.Panel.from_data_tables([data_table_with_index_and_all_headers])
    table_from_panel_with_index_and_all_headers = pl.Table.from_panel_list([panel_with_index_and_all_headers])
    data_table_with_index_all_headers_and_no_columns = pl.DataTable.from_df(
        EXAMPLE_DF,
        include_index=True,
        include_columns=False,
        extra_header='Header',
        top_left_corner_labels='TL Header'
    )
    panel_with_index_all_headers_and_no_columns = pl.Panel.from_data_tables([data_table_with_index_all_headers_and_no_columns])
    table_from_panel_with_index_all_headers_and_no_columns = pl.Table.from_panel_list([panel_with_index_all_headers_and_no_columns])
    dt_with_index_and_header_1 = pl.DataTable.from_df(
        EXAMPLE_DF,
        include_index=True,
        extra_header='DT 1',
    )
    dt_with_index_and_header_2 = pl.DataTable.from_df(
        (EXAMPLE_DF + 10),
        include_index=True,
        extra_header='DT 2',
    )
    dt_with_index_and_header_3 = pl.DataTable.from_df(
        (EXAMPLE_DF + 20),
        include_index=True,
        extra_header='DT 3',
    )
    dt_with_index_and_header_4 = pl.DataTable.from_df(
        (EXAMPLE_DF + 30),
        include_index=True,
        extra_header='DT 4',
    )
    dt_with_index_and_header_no_columns_1 = pl.DataTable.from_df(
        EXAMPLE_DF,
        include_index=True,
        include_columns=False,
        extra_header='DT 1',
    )
    dt_with_index_and_header_no_columns_2 = pl.DataTable.from_df(
        (EXAMPLE_DF + 10),
        include_index=True,
        include_columns=False,
        extra_header='DT 2',
    )
    dt_with_index_and_header_no_columns_3 = pl.DataTable.from_df(
        (EXAMPLE_DF + 20),
        include_index=True,
        include_columns=False,
        extra_header='DT 3',
    )
    dt_with_index_and_header_no_columns_4 = pl.DataTable.from_df(
        (EXAMPLE_DF + 30),
        include_index=True,
        include_columns=False,
        extra_header='DT 4',
    )
    dt_two_column_with_index_and_header_1 = pl.DataTable.from_df(
        EXAMPLE_DF[['a', 'b']],
        include_index=True,
        extra_header='DT 1',
    )
    dt_two_column_with_index_and_header_2 = pl.DataTable.from_df(
        (EXAMPLE_DF[['a', 'b']] + 10),
        include_index=True,
        extra_header='DT 2',
    )
    dt_with_index_header_and_tl_1 = pl.DataTable.from_df(
        EXAMPLE_DF,
        include_index=True,
        extra_header='DT 1',
        top_left_corner_labels='TL 1'
    )
    panel_one_from_two_data_tables_horizontal = pl.Panel.from_data_tables(
        [
            dt_with_index_and_header_1,
            dt_with_index_and_header_2
        ],
        shape=(1, 2),
        name='One'
    )
    panel_two_from_two_data_tables_horizontal = pl.Panel.from_data_tables(
        [
            dt_with_index_and_header_3,
            dt_with_index_and_header_4
        ],
        shape=(1, 2),
        name='Two'
    )
    table_from_dual_panel_dual_data_tables_horizontal = pl.Table.from_panel_list([
        panel_one_from_two_data_tables_horizontal,
        panel_two_from_two_data_tables_horizontal,
    ])
    panel_one_from_two_data_tables_no_columns_horizontal = pl.Panel.from_data_tables(
        [
            dt_with_index_and_header_no_columns_1,
            dt_with_index_and_header_no_columns_2,
        ],
        shape=(1, 2),
        name='One'
    )
    panel_two_from_two_data_tables_no_columns_horizontal = pl.Panel.from_data_tables(
        [
            dt_with_index_and_header_no_columns_3,
            dt_with_index_and_header_no_columns_4,
        ],
        shape=(1, 2),
        name='Two'
    )
    table_from_dual_panel_dual_data_tables_no_columns_horizontal = pl.Table.from_panel_list([
        panel_one_from_two_data_tables_no_columns_horizontal,
        panel_two_from_two_data_tables_no_columns_horizontal,
    ])
    panel_one_from_two_data_tables_vertical = pl.Panel.from_data_tables(
        [
            dt_with_index_and_header_1,
            dt_with_index_and_header_2
        ],
        shape=(2, 1),
        name='One'
    )
    panel_two_from_two_data_tables_vertical = pl.Panel.from_data_tables(
        [
            dt_with_index_and_header_3,
            dt_with_index_and_header_4
        ],
        shape=(2, 1),
        name='Two'
    )
    table_from_dual_panel_dual_data_tables_vertical = pl.Table.from_panel_list([
        panel_one_from_two_data_tables_vertical,
        panel_two_from_two_data_tables_vertical,
    ])
    panel_two_from_two_data_tables_two_column_vertical = pl.Panel.from_data_tables(
        [
            dt_two_column_with_index_and_header_1,
            dt_two_column_with_index_and_header_2,
        ],
        shape=(2, 1),
        name='Two'
    )
    table_from_dual_panel_dual_data_tables_vertical_subset_column_match = pl.Table.from_panel_list([
        panel_one_from_two_data_tables_vertical,
        panel_two_from_two_data_tables_two_column_vertical,
    ])
    panel_one_from_two_data_tables_with_tl_vertical = pl.Panel.from_data_tables(
        [
            dt_with_index_header_and_tl_1,
            dt_with_index_and_header_2
        ],
        shape=(2, 1),
        name='One'
    )
    table_from_dual_panel_dual_data_tables_with_tl_vertical_subset_column_match = pl.Table.from_panel_list([
        panel_one_from_two_data_tables_with_tl_vertical,
        panel_two_from_two_data_tables_two_column_vertical,
    ])

    def test_table(self):
        assert str(self.table) == '\\begin{table}\n\\centering\n\\begin{threeparttable}\n\\caption{My Table Title}\n\\begin{tabular}{lcc}\n\\toprule\na & b & c\\\\\n 1 &  2 &  3 \\\\\n 4 &  5 &  6 \\\\\n 7 &  8 &  9 \\\\\n\\bottomrule\n\n\\end{tabular}\n\\begin{tablenotes}[para, flushleft]\nMy below text\n\\end{tablenotes}\n\\end{threeparttable}\n\\end{table}'

    def test_two_panel_table_no_index(self):
        assert str(self.two_panel_table_from_dict_no_index) == str(self.two_panel_table_from_lol_no_index) == '\\begin{table}\n\\centering\n\\begin{threeparttable}\n\\caption{My Table Title}\n\\begin{tabular}{lcc}\n\\toprule\na & b & c\\\\\n\\midrule\n\\multicolumn{3}{l}{Panel A: One}\\\\\n 1 &  2 &  3 \\\\\n 4 &  5 &  6 \\\\\n 7 &  8 &  9 \\\\\n  &   &  \\\\\n\\multicolumn{3}{l}{Panel B: Two}\\\\\n 11 &  12 &  13 \\\\\n 14 &  15 &  16 \\\\\n 17 &  18 &  19 \\\\\n\\bottomrule\n\n\\end{tabular}\n\\begin{tablenotes}[para, flushleft]\nMy below text\n\\end{tablenotes}\n\\end{threeparttable}\n\\end{table}'

    def test_two_panel_table_no_index_with_tl(self):
        assert str(self.two_panel_table_from_dict_no_index_with_tl) == str(self.two_panel_table_from_lol_no_index_with_tl) == '\\begin{table}\n\\centering\n\\begin{threeparttable}\n\\caption{My Table Title}\n\\begin{tabular}{lccc}\n\\toprule\nwoo & a & b & c\\\\\n\\midrule\n\\multicolumn{4}{l}{Panel A: One}\\\\\n &  1 &  2 &  3 \\\\\n &  4 &  5 &  6 \\\\\n &  7 &  8 &  9 \\\\\n  &   &   &  \\\\\n\\multicolumn{4}{l}{Panel B: Two}\\\\\n &  11 &  12 &  13 \\\\\n &  14 &  15 &  16 \\\\\n &  17 &  18 &  19 \\\\\n\\bottomrule\n\n\\end{tabular}\n\\begin{tablenotes}[para, flushleft]\nMy below text\n\\end{tablenotes}\n\\end{threeparttable}\n\\end{table}'

    def test_two_panel_table_with_index(self):
        assert str(self.two_panel_table_from_dict_with_index) == str(self.two_panel_table_from_lol_with_index) == '\\begin{table}\n\\centering\n\\begin{threeparttable}\n\\caption{My Table Title}\n\\begin{tabular}{lccc}\n\\toprule\n  & a & b & c\\\\\n\\midrule\n\\multicolumn{4}{l}{Panel A: One}\\\\\n0 &  1 &  2 &  3 \\\\\n1 &  4 &  5 &  6 \\\\\n2 &  7 &  8 &  9 \\\\\n  &   &   &  \\\\\n\\multicolumn{4}{l}{Panel B: Two}\\\\\n0 &  11 &  12 &  13 \\\\\n1 &  14 &  15 &  16 \\\\\n2 &  17 &  18 &  19 \\\\\n\\bottomrule\n\n\\end{tabular}\n\\begin{tablenotes}[para, flushleft]\nMy below text\n\\end{tablenotes}\n\\end{threeparttable}\n\\end{table}'

    def test_two_panel_table_with_index_and_name(self):
        assert str(self.two_panel_table_from_dict_with_index_and_name) == str(self.two_panel_table_from_lol_with_index_and_name) == '\\begin{table}\n\\centering\n\\begin{threeparttable}\n\\caption{My Table Title}\n\\begin{tabular}{lccc}\n\\toprule\n  & a & b & c\\\\\n\\midrule\n\\multicolumn{4}{l}{Panel A: One}\\\\\n0 &  1 &  2 &  3 \\\\\n1 &  4 &  5 &  6 \\\\\n2 &  7 &  8 &  9 \\\\\n  &   &   &  \\\\\n\\multicolumn{4}{l}{Panel B: Two}\\\\\n0 &  11 &  12 &  13 \\\\\n1 &  14 &  15 &  16 \\\\\n2 &  17 &  18 &  19 \\\\\n\\bottomrule\n\n\\end{tabular}\n\\begin{tablenotes}[para, flushleft]\nMy below text\n\\end{tablenotes}\n\\end{threeparttable}\n\\end{table}'

    def test_two_panel_table_with_index_and_tl(self):
        assert str(self.two_panel_table_from_dict_with_index_and_tl) == str(self.two_panel_table_from_lol_with_index_and_tl) == '\\begin{table}\n\\centering\n\\begin{threeparttable}\n\\caption{My Table Title}\n\\begin{tabular}{lccc}\n\\toprule\nTL Label & a & b & c\\\\\n\\midrule\n\\multicolumn{4}{l}{Panel A: One}\\\\\n0 &  1 &  2 &  3 \\\\\n1 &  4 &  5 &  6 \\\\\n2 &  7 &  8 &  9 \\\\\n  &   &   &  \\\\\n\\multicolumn{4}{l}{Panel B: Two}\\\\\n0 &  11 &  12 &  13 \\\\\n1 &  14 &  15 &  16 \\\\\n2 &  17 &  18 &  19 \\\\\n\\bottomrule\n\n\\end{tabular}\n\\begin{tablenotes}[para, flushleft]\nMy below text\n\\end{tablenotes}\n\\end{threeparttable}\n\\end{table}'

    def test_two_panel_table_no_pad(self):
        assert str(self.two_panel_table_from_dict_no_pad) == str(self.two_panel_table_from_lol_no_pad) == '\\begin{table}\n\\centering\n\\begin{threeparttable}\n\\caption{My Table Title}\n\\begin{tabular}{lccc}\n\\toprule\n  & a & b & c\\\\\n\\midrule\n\\multicolumn{4}{l}{Panel A: One}\\\\\n0 &  1 &  2 &  3 \\\\\n1 &  4 &  5 &  6 \\\\\n2 &  7 &  8 &  9 \\\\\n\\midrule\n\\multicolumn{4}{l}{Panel B: Two}\\\\\n0 &  11 &  12 &  13 \\\\\n1 &  14 &  15 &  16 \\\\\n2 &  17 &  18 &  19 \\\\\n\\bottomrule\n\n\\end{tabular}\n\\begin{tablenotes}[para, flushleft]\nMy below text\n\\end{tablenotes}\n\\end{threeparttable}\n\\end{table}'

    def test_two_panel_table_double_pad(self):
        assert str(self.two_panel_table_from_dict_double_pad) == str(self.two_panel_table_from_lol_double_pad) == '\\begin{table}\n\\centering\n\\begin{threeparttable}\n\\caption{My Table Title}\n\\begin{tabular}{lccc}\n\\toprule\n  & a & b & c\\\\\n\\midrule\n\\multicolumn{4}{l}{Panel A: One}\\\\\n0 &  1 &  2 &  3 \\\\\n1 &  4 &  5 &  6 \\\\\n2 &  7 &  8 &  9 \\\\\n  &   &   &  \\\\\n  &   &   &  \\\\\n\\multicolumn{4}{l}{Panel B: Two}\\\\\n0 &  11 &  12 &  13 \\\\\n1 &  14 &  15 &  16 \\\\\n2 &  17 &  18 &  19 \\\\\n\\bottomrule\n\n\\end{tabular}\n\\begin{tablenotes}[para, flushleft]\nMy below text\n\\end{tablenotes}\n\\end{threeparttable}\n\\end{table}'

    def test_table_with_short_caption(self):
        assert str(self.table_from_dict_with_short_caption) == '\\begin{table}\n\\centering\n\\begin{threeparttable}\n\\caption[Short Capt]{My Table Title}\n\\begin{tabular}{lcc}\n\\toprule\na & b & c\\\\\n\\multicolumn{3}{l}{Panel A: One}\\\\\n 1 &  2 &  3 \\\\\n 4 &  5 &  6 \\\\\n 7 &  8 &  9 \\\\\n\\bottomrule\n\n\\end{tabular}\n\\begin{tablenotes}[para, flushleft]\nMy below text\n\\end{tablenotes}\n\\end{threeparttable}\n\\end{table}'
        assert str(self.table_from_lol_with_short_caption) == '\\begin{table}\n\\centering\n\\begin{threeparttable}\n\\caption[Short Capt]{My Table Title}\n\\begin{tabular}{lcc}\n\\toprule\na & b & c\\\\\n 1 &  2 &  3 \\\\\n 4 &  5 &  6 \\\\\n 7 &  8 &  9 \\\\\n\\bottomrule\n\n\\end{tabular}\n\\begin{tablenotes}[para, flushleft]\nMy below text\n\\end{tablenotes}\n\\end{threeparttable}\n\\end{table}'

    def test_table_with_siunitx_aligns(self):
        assert str(self.table_with_siunitx_aligns) == '\\begin{table}\n\\centering\n\\begin{threeparttable}\n\\caption{My Table Title}\n\\begin{tabular}{lS[table-column-width=4cm]s}\n\\toprule\na & b & c\\\\\n 1 &   2.540 &    3.100 \\\\\n 4 &  50.000 &  654.000 \\\\\n 7 &   8.114 &    9.541 \\\\\n\\bottomrule\n\n\\end{tabular}\n\\begin{tablenotes}[para, flushleft]\nMy below text\n\\end{tablenotes}\n\\end{threeparttable}\n\\end{table}'

    def test_table_with_dcolumn_aligns(self):
        assert str(self.table_with_dcolumn_aligns) == '\\begin{table}\n\\centering\n\\begin{threeparttable}\n\\caption{My Table Title}\n\\begin{tabular}{ld{2.3}D{.}{,}{3.3}}\n\\toprule\na & b & c\\\\\n 1 &   2.540 &    3.100 \\\\\n 4 &  50.000 &  654.000 \\\\\n 7 &   8.114 &    9.541 \\\\\n\\bottomrule\n\n\\end{tabular}\n\\begin{tablenotes}[para, flushleft]\nMy below text\n\\end{tablenotes}\n\\end{threeparttable}\n\\end{table}'

    def test_table_with_spacing_adjust_aligns(self):
        assert str(self.table_with_spacing_adjust_aligns) == '\\begin{table}\n\\centering\n\\begin{threeparttable}\n\\caption{My Table Title}\n\\begin{tabular}{@{}l!{}c@{}c@{}}\n\\toprule\na & b & c\\\\\n 1 &   2.540 &    3.100 \\\\\n 4 &  50.000 &  654.000 \\\\\n 7 &   8.114 &    9.541 \\\\\n\\bottomrule\n\n\\end{tabular}\n\\begin{tablenotes}[para, flushleft]\nMy below text\n\\end{tablenotes}\n\\end{threeparttable}\n\\end{table}'

    def test_table_with_position_str(self):
        assert str(self.table_with_position_str) == '\\begin{table}[htb]\n\\centering\n\\begin{threeparttable}\n\\caption{My Table Title}\n\\begin{tabular}{lcc}\n\\toprule\na & b & c\\\\\n 1 &  2 &  3 \\\\\n 4 &  5 &  6 \\\\\n 7 &  8 &  9 \\\\\n\\bottomrule\n\n\\end{tabular}\n\\begin{tablenotes}[para, flushleft]\nMy below text\n\\end{tablenotes}\n\\end{threeparttable}\n\\end{table}'

    def test_table_to_tabular(self):
        tabular = self.two_panel_table_from_lol_with_index.tex_obj(as_document=False, as_single_tabular=True)
        assert str(tabular) == '\\begin{tabular}{lccc}\n\\toprule\n  & a & b & c\\\\\n\\midrule\n\\multicolumn{4}{l}{Panel A: One}\\\\\n0 &  1 &  2 &  3 \\\\\n1 &  4 &  5 &  6 \\\\\n2 &  7 &  8 &  9 \\\\\n  &   &   &  \\\\\n\\multicolumn{4}{l}{Panel B: Two}\\\\\n0 &  11 &  12 &  13 \\\\\n1 &  14 &  15 &  16 \\\\\n2 &  17 &  18 &  19 \\\\\n\\bottomrule\n\n\\end{tabular}'

    def test_table_to_tabular_list(self):
        tabular_list = self.two_panel_table_from_lol_with_index.tex_obj(as_document=False, as_panel_tabular_list=True)
        assert len(tabular_list) == 2
        assert isinstance(tabular_list, list)
        assert str(tabular_list[0]) == '\\begin{tabular}{lccc}\n\\toprule\n\\multicolumn{4}{l}{Panel A: One}\\\\\n  & a & b & c\\\\\n\\midrule\n0 &  1 &  2 &  3 \\\\\n1 &  4 &  5 &  6 \\\\\n2 &  7 &  8 &  9 \\\\\n\\bottomrule\n\n\\end{tabular}'
        assert str(tabular_list[1]) == '\\begin{tabular}{lccc}\n\\toprule\n\\multicolumn{4}{l}{Panel A: Two}\\\\\n  & a & b & c\\\\\n\\midrule\n0 &  11 &  12 &  13 \\\\\n1 &  14 &  15 &  16 \\\\\n2 &  17 &  18 &  19 \\\\\n\\bottomrule\n\n\\end{tabular}'

    def test_table_with_tl(self):
        assert str(self.table_with_tl) == '\\begin{table}\n\\centering\n\\begin{threeparttable}\n\\caption{My Table Title}\n\\begin{tabular}{lccc}\n\\toprule\nTL Header & a & b & c\\\\\n\\midrule\n &  1 &  2 &  3 \\\\\n &  4 &  5 &  6 \\\\\n &  7 &  8 &  9 \\\\\n\\bottomrule\n\n\\end{tabular}\n\\end{threeparttable}\n\\end{table}'

    def test_table_from_panel_with_index_and_tl(self):
        assert str(self.table_from_panel_with_index_and_tl) == '\\begin{table}\n\\centering\n\\begin{threeparttable}\n\\caption{}\n\\begin{tabular}{lccc}\n\\toprule\nTL Header & a & b & c\\\\\n\\midrule\n0 &  1 &  2 &  3 \\\\\n1 &  4 &  5 &  6 \\\\\n2 &  7 &  8 &  9 \\\\\n\\bottomrule\n\n\\end{tabular}\n\\end{threeparttable}\n\\end{table}'

    def test_table_from_panel_with_index_and_all_headers(self):
        assert str(self.table_from_panel_with_index_and_all_headers) == '\\begin{table}\n\\centering\n\\begin{threeparttable}\n\\caption{}\n\\begin{tabular}{lccc}\n\\toprule\n & \\multicolumn{3}{c}{Header}\\\\\n\\cmidrule(lr){2-4}\nTL Header & a & b & c\\\\\n\\midrule\n0 &  1 &  2 &  3 \\\\\n1 &  4 &  5 &  6 \\\\\n2 &  7 &  8 &  9 \\\\\n\\bottomrule\n\n\\end{tabular}\n\\end{threeparttable}\n\\end{table}'

    def test_table_from_panel_with_index_all_headers_and_no_columns(self):
        assert str(self.table_from_panel_with_index_all_headers_and_no_columns) == '\\begin{table}\n\\centering\n\\begin{threeparttable}\n\\caption{}\n\\begin{tabular}{lccc}\n\\toprule\nTL Header & \\multicolumn{3}{c}{Header}\\\\\n\\cmidrule(lr){2-4}\n\\midrule\n0 &  1 &  2 &  3 \\\\\n1 &  4 &  5 &  6 \\\\\n2 &  7 &  8 &  9 \\\\\n\\bottomrule\n\n\\end{tabular}\n\\end{threeparttable}\n\\end{table}'

    def test_table_from_dual_panel_dual_data_tables_horizontal(self):
        assert str(self.table_from_dual_panel_dual_data_tables_horizontal) == '\\begin{table}\n\\centering\n\\begin{threeparttable}\n\\caption{}\n\\begin{tabular}{lccccccc}\n\\toprule\n  & a & b & c &   & a & b & c\\\\\n\\midrule\n\\multicolumn{8}{l}{Panel A: One}\\\\\n  & \\multicolumn{3}{c}{DT 1} &   & \\multicolumn{3}{c}{DT 2}\\\\\n\\cmidrule(lr){2-4} \\cmidrule(lr){6-8}\n0 &  1 &  2 &  3  &   &  11 &  12 &  13 \\\\\n1 &  4 &  5 &  6  &   &  14 &  15 &  16 \\\\\n2 &  7 &  8 &  9  &   &  17 &  18 &  19 \\\\\n  &   &   &   &   &   &   &  \\\\\n\\multicolumn{8}{l}{Panel B: Two}\\\\\n  & \\multicolumn{3}{c}{DT 3} &   & \\multicolumn{3}{c}{DT 4}\\\\\n\\cmidrule(lr){2-4} \\cmidrule(lr){6-8}\n0 &  21 &  22 &  23  &   &  31 &  32 &  33 \\\\\n1 &  24 &  25 &  26  &   &  34 &  35 &  36 \\\\\n2 &  27 &  28 &  29  &   &  37 &  38 &  39 \\\\\n\\bottomrule\n\n\\end{tabular}\n\\end{threeparttable}\n\\end{table}'

    def test_table_from_dual_panel_dual_data_tables_no_columns_horizontal(self):
        assert str(self.table_from_dual_panel_dual_data_tables_no_columns_horizontal) == '\\begin{table}\n\\centering\n\\begin{threeparttable}\n\\caption{}\n\\begin{tabular}{lccccccc}\n\\toprule\n\\multicolumn{8}{l}{Panel A: One}\\\\\n  & \\multicolumn{3}{c}{DT 1} &   & \\multicolumn{3}{c}{DT 2}\\\\\n\\cmidrule(lr){2-4} \\cmidrule(lr){6-8}\n0 &  1 &  2 &  3  &   &  11 &  12 &  13 \\\\\n1 &  4 &  5 &  6  &   &  14 &  15 &  16 \\\\\n2 &  7 &  8 &  9  &   &  17 &  18 &  19 \\\\\n  &   &   &   &   &   &   &  \\\\\n\\multicolumn{8}{l}{Panel B: Two}\\\\\n  & \\multicolumn{3}{c}{DT 3} &   & \\multicolumn{3}{c}{DT 4}\\\\\n\\cmidrule(lr){2-4} \\cmidrule(lr){6-8}\n0 &  21 &  22 &  23  &   &  31 &  32 &  33 \\\\\n1 &  24 &  25 &  26  &   &  34 &  35 &  36 \\\\\n2 &  27 &  28 &  29  &   &  37 &  38 &  39 \\\\\n\\bottomrule\n\n\\end{tabular}\n\\end{threeparttable}\n\\end{table}'

    def test_table_from_dual_panel_dual_data_tables_vertical(self):
        assert str(self.table_from_dual_panel_dual_data_tables_vertical) == '\\begin{table}\n\\centering\n\\begin{threeparttable}\n\\caption{}\n\\begin{tabular}{lccc}\n\\toprule\n  & a & b & c\\\\\n\\midrule\n\\multicolumn{4}{l}{Panel A: One}\\\\\n  & \\multicolumn{3}{c}{DT 1}\\\\\n\\cmidrule(lr){2-4}\n0 &  1 &  2 &  3 \\\\\n1 &  4 &  5 &  6 \\\\\n2 &  7 &  8 &  9 \\\\\n  &   &   &  \\\\\n  & \\multicolumn{3}{c}{DT 2}\\\\\n\\cmidrule(lr){2-4}\n0 &  11 &  12 &  13 \\\\\n1 &  14 &  15 &  16 \\\\\n2 &  17 &  18 &  19 \\\\\n  &   &   &  \\\\\n\\multicolumn{4}{l}{Panel B: Two}\\\\\n  & \\multicolumn{3}{c}{DT 3}\\\\\n\\cmidrule(lr){2-4}\n0 &  21 &  22 &  23 \\\\\n1 &  24 &  25 &  26 \\\\\n2 &  27 &  28 &  29 \\\\\n  &   &   &  \\\\\n  & \\multicolumn{3}{c}{DT 4}\\\\\n\\cmidrule(lr){2-4}\n0 &  31 &  32 &  33 \\\\\n1 &  34 &  35 &  36 \\\\\n2 &  37 &  38 &  39 \\\\\n\\bottomrule\n\n\\end{tabular}\n\\end{threeparttable}\n\\end{table}'

    def test_table_from_dual_panel_dual_data_tables_vertical_subset_column_match(self):
        assert str(self.table_from_dual_panel_dual_data_tables_vertical_subset_column_match) == '\\begin{table}\n\\centering\n\\begin{threeparttable}\n\\caption{}\n\\begin{tabular}{lccc}\n\\toprule\n  & a & b & c\\\\\n\\midrule\n\\multicolumn{4}{l}{Panel A: One}\\\\\n  & \\multicolumn{3}{c}{DT 1}\\\\\n\\cmidrule(lr){2-4}\n0 &  1 &  2 &  3 \\\\\n1 &  4 &  5 &  6 \\\\\n2 &  7 &  8 &  9 \\\\\n  &   &   &  \\\\\n  & \\multicolumn{3}{c}{DT 2}\\\\\n\\cmidrule(lr){2-4}\n0 &  11 &  12 &  13 \\\\\n1 &  14 &  15 &  16 \\\\\n2 &  17 &  18 &  19 \\\\\n  &   &   &  \\\\\n\\multicolumn{3}{l}{Panel B: Two}\\\\\n  & \\multicolumn{2}{c}{DT 1} &  \\\\\n\\cmidrule(lr){2-3}\n0 &  1 &  2  &  \\\\\n1 &  4 &  5  &  \\\\\n2 &  7 &  8  &  \\\\\n  &   &   &  \\\\\n  & \\multicolumn{2}{c}{DT 2} &  \\\\\n\\cmidrule(lr){2-3}\n0 &  11 &  12  &  \\\\\n1 &  14 &  15  &  \\\\\n2 &  17 &  18  &  \\\\\n\\bottomrule\n\n\\end{tabular}\n\\end{threeparttable}\n\\end{table}'

    def test_table_from_dual_panel_dual_data_tables_with_tl_vertical_subset_column_match(self):
        assert str(self.table_from_dual_panel_dual_data_tables_with_tl_vertical_subset_column_match) == '\\begin{table}\n\\centering\n\\begin{threeparttable}\n\\caption{}\n\\begin{tabular}{lccc}\n\\toprule\n\\multicolumn{4}{l}{Panel A: One}\\\\\n  & \\multicolumn{3}{c}{DT 1}\\\\\n\\cmidrule(lr){2-4}\nTL 1 & a & b & c\\\\\n0 &  1 &  2 &  3 \\\\\n1 &  4 &  5 &  6 \\\\\n2 &  7 &  8 &  9 \\\\\n  &   &   &  \\\\\n  & \\multicolumn{3}{c}{DT 2}\\\\\n\\cmidrule(lr){2-4}\n  & a & b & c\\\\\n0 &  11 &  12 &  13 \\\\\n1 &  14 &  15 &  16 \\\\\n2 &  17 &  18 &  19 \\\\\n  &   &   &  \\\\\n\\multicolumn{3}{l}{Panel B: Two}\\\\\n  & \\multicolumn{2}{c}{DT 1} &  \\\\\n\\cmidrule(lr){2-3}\n  & a & b &  \\\\\n0 &  1 &  2  &  \\\\\n1 &  4 &  5  &  \\\\\n2 &  7 &  8  &  \\\\\n  &   &   &  \\\\\n  & \\multicolumn{2}{c}{DT 2} &  \\\\\n\\cmidrule(lr){2-3}\n  & a & b &  \\\\\n0 &  11 &  12  &  \\\\\n1 &  14 &  15  &  \\\\\n2 &  17 &  18  &  \\\\\n\\bottomrule\n\n\\end{tabular}\n\\end{threeparttable}\n\\end{table}'

    def test_table_in_document(self):
        doc = pl.Document([self.table])
        assert str(doc) == '\\documentclass[]{article}\n\\usepackage{amsmath}\n\\usepackage{pdflscape}\n\\usepackage{booktabs}\n\\usepackage{array}\n\\usepackage{threeparttable}\n\\usepackage{fancyhdr}\n\\usepackage{lastpage}\n\\usepackage{textcomp}\n\\usepackage{dcolumn}\n\\newcolumntype{L}[1]{>{\\raggedright\\let\\newline\\\\\\arraybackslash\\hspace{0pt}}m{#1}}\n\\newcolumntype{C}[1]{>{\\centering\\let\\newline\\\\\\arraybackslash\\hspace{0pt}}m{#1}}\n\\newcolumntype{R}[1]{>{\\raggedleft\\let\\newline\\\\\\arraybackslash\\hspace{0pt}}m{#1}}\n\\newcolumntype{.}{D{.}{.}{-1}}\n\\newcolumntype{d}[1]{D{.}{.}{#1}}\n\\usepackage[T1]{fontenc}\n\\usepackage{caption}\n\\usepackage{subcaption}\n\\usepackage{graphicx}\n\\usepackage[margin=0.8in, bottom=1.2in]{geometry}\n\\usepackage[page]{appendix}\n\\pagestyle{fancy}\n\\renewcommand{\\headrulewidth}{0pt}\n\\fancyhead{}\n\\rfoot{Page \\thepage\\  of \\pageref{LastPage}}\n\\cfoot{}\n\\begin{document}\n\\begin{table}\n\\centering\n\\begin{threeparttable}\n\\caption{My Table Title}\n\\begin{tabular}{lcc}\n\\toprule\na & b & c\\\\\n 1 &  2 &  3 \\\\\n 4 &  5 &  6 \\\\\n 7 &  8 &  9 \\\\\n\\bottomrule\n\n\\end{tabular}\n\\begin{tablenotes}[para, flushleft]\nMy below text\n\\end{tablenotes}\n\\end{threeparttable}\n\\end{table}\n\\end{document}'
        name = 'document with table'
        doc.to_pdf(outfolder=GENERATED_FILES_DIR, outname=name)
        compare_pdfs_in_generated_vs_input_by_name(name)

    def test_two_panel_table_in_document(self):
        doc = pl.Document([self.two_panel_table_from_lol_with_index])
        assert str(doc) == '\\documentclass[]{article}\n\\usepackage{amsmath}\n\\usepackage{pdflscape}\n\\usepackage{booktabs}\n\\usepackage{array}\n\\usepackage{threeparttable}\n\\usepackage{fancyhdr}\n\\usepackage{lastpage}\n\\usepackage{textcomp}\n\\usepackage{dcolumn}\n\\newcolumntype{L}[1]{>{\\raggedright\\let\\newline\\\\\\arraybackslash\\hspace{0pt}}m{#1}}\n\\newcolumntype{C}[1]{>{\\centering\\let\\newline\\\\\\arraybackslash\\hspace{0pt}}m{#1}}\n\\newcolumntype{R}[1]{>{\\raggedleft\\let\\newline\\\\\\arraybackslash\\hspace{0pt}}m{#1}}\n\\newcolumntype{.}{D{.}{.}{-1}}\n\\newcolumntype{d}[1]{D{.}{.}{#1}}\n\\usepackage[T1]{fontenc}\n\\usepackage{caption}\n\\usepackage{subcaption}\n\\usepackage{graphicx}\n\\usepackage[margin=0.8in, bottom=1.2in]{geometry}\n\\usepackage[page]{appendix}\n\\pagestyle{fancy}\n\\renewcommand{\\headrulewidth}{0pt}\n\\fancyhead{}\n\\rfoot{Page \\thepage\\  of \\pageref{LastPage}}\n\\cfoot{}\n\\begin{document}\n\\begin{table}\n\\centering\n\\begin{threeparttable}\n\\caption{My Table Title}\n\\begin{tabular}{lccc}\n\\toprule\n  & a & b & c\\\\\n\\midrule\n\\multicolumn{4}{l}{Panel A: One}\\\\\n0 &  1 &  2 &  3 \\\\\n1 &  4 &  5 &  6 \\\\\n2 &  7 &  8 &  9 \\\\\n  &   &   &  \\\\\n\\multicolumn{4}{l}{Panel B: Two}\\\\\n0 &  11 &  12 &  13 \\\\\n1 &  14 &  15 &  16 \\\\\n2 &  17 &  18 &  19 \\\\\n\\bottomrule\n\n\\end{tabular}\n\\begin{tablenotes}[para, flushleft]\nMy below text\n\\end{tablenotes}\n\\end{threeparttable}\n\\end{table}\n\\end{document}'
        name = 'document with two panel table'
        doc.to_pdf(outfolder=GENERATED_FILES_DIR, outname=name)
        compare_pdfs_in_generated_vs_input_by_name(name)

    def test_siunitx_table_in_document(self):
        doc = pl.Document([self.table_with_siunitx_aligns])
        assert str(doc) == '\\documentclass[]{article}\n\\usepackage{amsmath}\n\\usepackage{pdflscape}\n\\usepackage{booktabs}\n\\usepackage{array}\n\\usepackage{threeparttable}\n\\usepackage{fancyhdr}\n\\usepackage{lastpage}\n\\usepackage{textcomp}\n\\usepackage{dcolumn}\n\\newcolumntype{L}[1]{>{\\raggedright\\let\\newline\\\\\\arraybackslash\\hspace{0pt}}m{#1}}\n\\newcolumntype{C}[1]{>{\\centering\\let\\newline\\\\\\arraybackslash\\hspace{0pt}}m{#1}}\n\\newcolumntype{R}[1]{>{\\raggedleft\\let\\newline\\\\\\arraybackslash\\hspace{0pt}}m{#1}}\n\\newcolumntype{.}{D{.}{.}{-1}}\n\\newcolumntype{d}[1]{D{.}{.}{#1}}\n\\usepackage[T1]{fontenc}\n\\usepackage{caption}\n\\usepackage{subcaption}\n\\usepackage{graphicx}\n\\usepackage[margin=0.8in, bottom=1.2in]{geometry}\n\\usepackage[page]{appendix}\n\\usepackage{siunitx}\n\\pagestyle{fancy}\n\\renewcommand{\\headrulewidth}{0pt}\n\\fancyhead{}\n\\rfoot{Page \\thepage\\  of \\pageref{LastPage}}\n\\cfoot{}\n\\begin{document}\n\\begin{table}\n\\centering\n\\begin{threeparttable}\n\\caption{My Table Title}\n\\begin{tabular}{lS[table-column-width=4cm]s}\n\\toprule\na & b & c\\\\\n 1 &   2.540 &    3.100 \\\\\n 4 &  50.000 &  654.000 \\\\\n 7 &   8.114 &    9.541 \\\\\n\\bottomrule\n\n\\end{tabular}\n\\begin{tablenotes}[para, flushleft]\nMy below text\n\\end{tablenotes}\n\\end{threeparttable}\n\\end{table}\n\\end{document}'
        name = 'document with siunitx table'
        doc.to_pdf(outfolder=GENERATED_FILES_DIR, outname=name)
        compare_pdfs_in_generated_vs_input_by_name(name)

    def test_dcolumn_table_in_document(self):
        doc = pl.Document([self.table_with_dcolumn_aligns])
        assert str(doc) == '\\documentclass[]{article}\n\\usepackage{amsmath}\n\\usepackage{pdflscape}\n\\usepackage{booktabs}\n\\usepackage{array}\n\\usepackage{threeparttable}\n\\usepackage{fancyhdr}\n\\usepackage{lastpage}\n\\usepackage{textcomp}\n\\usepackage{dcolumn}\n\\newcolumntype{L}[1]{>{\\raggedright\\let\\newline\\\\\\arraybackslash\\hspace{0pt}}m{#1}}\n\\newcolumntype{C}[1]{>{\\centering\\let\\newline\\\\\\arraybackslash\\hspace{0pt}}m{#1}}\n\\newcolumntype{R}[1]{>{\\raggedleft\\let\\newline\\\\\\arraybackslash\\hspace{0pt}}m{#1}}\n\\newcolumntype{.}{D{.}{.}{-1}}\n\\newcolumntype{d}[1]{D{.}{.}{#1}}\n\\usepackage[T1]{fontenc}\n\\usepackage{caption}\n\\usepackage{subcaption}\n\\usepackage{graphicx}\n\\usepackage[margin=0.8in, bottom=1.2in]{geometry}\n\\usepackage[page]{appendix}\n\\pagestyle{fancy}\n\\renewcommand{\\headrulewidth}{0pt}\n\\fancyhead{}\n\\rfoot{Page \\thepage\\  of \\pageref{LastPage}}\n\\cfoot{}\n\\begin{document}\n\\begin{table}\n\\centering\n\\begin{threeparttable}\n\\caption{My Table Title}\n\\begin{tabular}{ld{2.3}D{.}{,}{3.3}}\n\\toprule\na & b & c\\\\\n 1 &   2.540 &    3.100 \\\\\n 4 &  50.000 &  654.000 \\\\\n 7 &   8.114 &    9.541 \\\\\n\\bottomrule\n\n\\end{tabular}\n\\begin{tablenotes}[para, flushleft]\nMy below text\n\\end{tablenotes}\n\\end{threeparttable}\n\\end{table}\n\\end{document}'
        name = 'document with dcolumn table'
        doc.to_pdf(outfolder=GENERATED_FILES_DIR, outname=name)
        compare_pdfs_in_generated_vs_input_by_name(name)

    def test_spacing_adjust_aligns_table_in_document(self):
        doc = pl.Document([self.table_with_spacing_adjust_aligns])
        assert str(doc) == '\\documentclass[]{article}\n\\usepackage{amsmath}\n\\usepackage{pdflscape}\n\\usepackage{booktabs}\n\\usepackage{array}\n\\usepackage{threeparttable}\n\\usepackage{fancyhdr}\n\\usepackage{lastpage}\n\\usepackage{textcomp}\n\\usepackage{dcolumn}\n\\newcolumntype{L}[1]{>{\\raggedright\\let\\newline\\\\\\arraybackslash\\hspace{0pt}}m{#1}}\n\\newcolumntype{C}[1]{>{\\centering\\let\\newline\\\\\\arraybackslash\\hspace{0pt}}m{#1}}\n\\newcolumntype{R}[1]{>{\\raggedleft\\let\\newline\\\\\\arraybackslash\\hspace{0pt}}m{#1}}\n\\newcolumntype{.}{D{.}{.}{-1}}\n\\newcolumntype{d}[1]{D{.}{.}{#1}}\n\\usepackage[T1]{fontenc}\n\\usepackage{caption}\n\\usepackage{subcaption}\n\\usepackage{graphicx}\n\\usepackage[margin=0.8in, bottom=1.2in]{geometry}\n\\usepackage[page]{appendix}\n\\pagestyle{fancy}\n\\renewcommand{\\headrulewidth}{0pt}\n\\fancyhead{}\n\\rfoot{Page \\thepage\\  of \\pageref{LastPage}}\n\\cfoot{}\n\\begin{document}\n\\begin{table}\n\\centering\n\\begin{threeparttable}\n\\caption{My Table Title}\n\\begin{tabular}{@{}l!{}c@{}c@{}}\n\\toprule\na & b & c\\\\\n 1 &   2.540 &    3.100 \\\\\n 4 &  50.000 &  654.000 \\\\\n 7 &   8.114 &    9.541 \\\\\n\\bottomrule\n\n\\end{tabular}\n\\begin{tablenotes}[para, flushleft]\nMy below text\n\\end{tablenotes}\n\\end{threeparttable}\n\\end{table}\n\\end{document}'
        name = 'document with spacing adjust aligns table'
        doc.to_pdf(outfolder=GENERATED_FILES_DIR, outname=name)
        compare_pdfs_in_generated_vs_input_by_name(name)
