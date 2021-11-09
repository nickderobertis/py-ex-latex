from copy import deepcopy

import pandas as pd

import pyexlatex as pl
from tests.base import GENERATED_FILES_DIR
from tests.utils.generate import assert_same_or_generate_table, assert_same_or_generate_document
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
        assert_same_or_generate_table(self.table, "table")

    def test_two_panel_table_no_index(self):
        assert_same_or_generate_table(self.two_panel_table_from_dict_no_index, "two_panel_table_from_dict_no_index")

    def test_two_panel_table_no_index_with_tl(self):
        assert_same_or_generate_table(self.two_panel_table_from_dict_no_index_with_tl, "two_panel_table_from_dict_no_index_with_tl")

    def test_two_panel_table_with_index(self):
        assert_same_or_generate_table(self.two_panel_table_from_dict_with_index, "two_panel_table_from_dict_with_index")

    def test_two_panel_table_with_index_and_name(self):
        assert_same_or_generate_table(self.two_panel_table_from_dict_with_index_and_name, "two_panel_table_from_dict_with_index_and_name")

    def test_two_panel_table_with_index_and_tl(self):
        assert_same_or_generate_table(self.two_panel_table_from_dict_with_index_and_tl,
                                      "two_panel_table_with_index_and_tl")
        assert_same_or_generate_table(self.two_panel_table_from_lol_with_index_and_tl,
                                      "two_panel_table_with_index_and_tl")

    def test_two_panel_table_no_pad(self):
        assert_same_or_generate_table(self.two_panel_table_from_dict_no_pad, "two_panel_table_no_pad")
        assert_same_or_generate_table(self.two_panel_table_from_lol_no_pad, "two_panel_table_no_pad")

    def test_two_panel_table_double_pad(self):
        assert_same_or_generate_table(self.two_panel_table_from_dict_double_pad, "two_panel_table_double_pad")
        assert_same_or_generate_table(self.two_panel_table_from_lol_double_pad, "two_panel_table_double_pad")

    def test_table_with_short_caption(self):
        assert_same_or_generate_table(self.table_from_dict_with_short_caption, "table_from_dict_with_short_caption")
        assert_same_or_generate_table(self.table_from_lol_with_short_caption, "table_from_lol_with_short_caption")

    def test_table_with_siunitx_aligns(self):
        assert_same_or_generate_table(self.table_with_siunitx_aligns, "table_with_siunitx_aligns")

    def test_table_with_dcolumn_aligns(self):
        assert_same_or_generate_table(self.table_with_dcolumn_aligns, "table_with_dcolumn_aligns")

    def test_table_with_spacing_adjust_aligns(self):
        assert_same_or_generate_table(self.table_with_spacing_adjust_aligns, "table_with_spacing_adjust_aligns")

    def test_table_with_position_str(self):
        assert_same_or_generate_table(self.table_with_position_str, "table_with_position_str")

    def test_table_to_tabular(self):
        tabular = self.two_panel_table_from_lol_with_index.tex_obj(as_document=False, as_single_tabular=True)
        assert_same_or_generate_table(tabular, "table_to_tabular")

    def test_table_to_tabular_list(self):
        tabular_list = self.two_panel_table_from_lol_with_index.tex_obj(as_document=False, as_panel_tabular_list=True)
        assert len(tabular_list) == 2
        assert isinstance(tabular_list, list)
        assert_same_or_generate_table(tabular_list[0], "table_to_tabular_list_1")
        assert_same_or_generate_table(tabular_list[1], "table_to_tabular_list_2")

    def test_table_with_tl(self):
        assert_same_or_generate_table(self.table_with_tl, "table_with_tl")

    def test_table_from_panel_with_index_and_tl(self):
        assert_same_or_generate_table(self.table_from_panel_with_index_and_tl, "table_from_panel_with_index_and_tl")

    def test_table_from_panel_with_index_and_all_headers(self):
        assert_same_or_generate_table(self.table_from_panel_with_index_and_all_headers, "table_from_panel_with_index_and_all_headers")

    def test_table_from_panel_with_index_all_headers_and_no_columns(self):
        assert_same_or_generate_table(self.table_from_panel_with_index_all_headers_and_no_columns, "table_from_panel_with_index_all_headers_and_no_columns")

    def test_table_from_dual_panel_dual_data_tables_horizontal(self):
        assert_same_or_generate_table(self.table_from_dual_panel_dual_data_tables_horizontal, "table_from_dual_panel_dual_data_tables_horizontal")

    def test_table_from_dual_panel_dual_data_tables_no_columns_horizontal(self):
        assert_same_or_generate_table(self.table_from_dual_panel_dual_data_tables_no_columns_horizontal, "table_from_dual_panel_dual_data_tables_no_columns_horizontal")

    def test_table_from_dual_panel_dual_data_tables_vertical(self):
        assert_same_or_generate_table(self.table_from_dual_panel_dual_data_tables_vertical, "table_from_dual_panel_dual_data_tables_vertical")

    def test_table_from_dual_panel_dual_data_tables_vertical_subset_column_match(self):
        assert_same_or_generate_table(self.table_from_dual_panel_dual_data_tables_vertical_subset_column_match, "table_from_dual_panel_dual_data_tables_vertical_subset_column_match")

    def test_table_from_dual_panel_dual_data_tables_with_tl_vertical_subset_column_match(self):
        assert_same_or_generate_table(self.table_from_dual_panel_dual_data_tables_with_tl_vertical_subset_column_match, "table_from_dual_panel_dual_data_tables_with_tl_vertical_subset_column_match")

    def test_table_in_document(self):
        doc = pl.Document([self.table])
        name = 'document with table'
        assert_same_or_generate_document(doc, name)
        doc.to_pdf(outfolder=GENERATED_FILES_DIR, outname=name)
        compare_pdfs_in_generated_vs_input_by_name(name)

    def test_two_panel_table_in_document(self):
        doc = pl.Document([self.two_panel_table_from_lol_with_index])
        name = 'document with two panel table'
        assert_same_or_generate_document(doc, name)
        doc.to_pdf(outfolder=GENERATED_FILES_DIR, outname=name)
        compare_pdfs_in_generated_vs_input_by_name(name)

    def test_siunitx_table_in_document(self):
        doc = pl.Document([self.table_with_siunitx_aligns])
        name = 'document with siunitx table'
        assert_same_or_generate_document(doc, name)
        doc.to_pdf(outfolder=GENERATED_FILES_DIR, outname=name)
        compare_pdfs_in_generated_vs_input_by_name(name)

    def test_dcolumn_table_in_document(self):
        doc = pl.Document([self.table_with_dcolumn_aligns])
        name = 'document with dcolumn table'
        assert_same_or_generate_document(doc, name)
        doc.to_pdf(outfolder=GENERATED_FILES_DIR, outname=name)
        compare_pdfs_in_generated_vs_input_by_name(name)

    def test_spacing_adjust_aligns_table_in_document(self):
        doc = pl.Document([self.table_with_spacing_adjust_aligns])
        name = 'document with spacing adjust aligns table'
        assert_same_or_generate_document(doc, name)
        doc.to_pdf(outfolder=GENERATED_FILES_DIR, outname=name)
        compare_pdfs_in_generated_vs_input_by_name(name)
