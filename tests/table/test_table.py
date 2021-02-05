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

    def test_table_to_tabular(self):
        tabular = self.two_panel_table_from_lol_with_index.tex_obj(as_document=False, as_single_tabular=True)
        assert str(tabular) == '\\begin{tabular}{lccc}\n\\toprule\n  & a & b & c\\\\\n\\midrule\n\\multicolumn{4}{l}{Panel A: One}\\\\\n0 &  1 &  2 &  3 \\\\\n1 &  4 &  5 &  6 \\\\\n2 &  7 &  8 &  9 \\\\\n  &   &   &  \\\\\n\\multicolumn{4}{l}{Panel B: Two}\\\\\n0 &  11 &  12 &  13 \\\\\n1 &  14 &  15 &  16 \\\\\n2 &  17 &  18 &  19 \\\\\n\\bottomrule\n\n\\end{tabular}'

    def test_table_to_tabular_list(self):
        tabular_list = self.two_panel_table_from_lol_with_index.tex_obj(as_document=False, as_panel_tabular_list=True)
        assert len(tabular_list) == 2
        assert isinstance(tabular_list, list)
        assert str(tabular_list[0]) == '\\begin{tabular}{lccc}\n\\toprule\n\\multicolumn{4}{l}{Panel A: One}\\\\\n  & a & b & c\\\\\n\\midrule\n0 &  1 &  2 &  3 \\\\\n1 &  4 &  5 &  6 \\\\\n2 &  7 &  8 &  9 \\\\\n\\bottomrule\n\n\\end{tabular}'
        assert str(tabular_list[1]) == '\\begin{tabular}{lccc}\n\\toprule\n\\multicolumn{4}{l}{Panel A: Two}\\\\\n  & a & b & c\\\\\n\\midrule\n0 &  11 &  12 &  13 \\\\\n1 &  14 &  15 &  16 \\\\\n2 &  17 &  18 &  19 \\\\\n\\bottomrule\n\n\\end{tabular}'

    def test_table_in_document(self):
        doc = pl.Document([self.table])
        assert str(doc) == '\\documentclass[]{article}\n\\usepackage{threeparttable}\n\\usepackage{booktabs}\n\\usepackage{dcolumn}\n\\newcolumntype{L}[1]{>{\\raggedright\\let\\newline\\\\\\arraybackslash\\hspace{0pt}}m{#1}}\n\\newcolumntype{C}[1]{>{\\centering\\let\\newline\\\\\\arraybackslash\\hspace{0pt}}m{#1}}\n\\newcolumntype{R}[1]{>{\\raggedleft\\let\\newline\\\\\\arraybackslash\\hspace{0pt}}m{#1}}\n\\newcolumntype{.}{D{.}{.}{-1}}\n\\usepackage{amsmath}\n\\usepackage{pdflscape}\n\\usepackage{array}\n\\usepackage{fancyhdr}\n\\usepackage{lastpage}\n\\usepackage{textcomp}\n\\usepackage[T1]{fontenc}\n\\usepackage{caption}\n\\usepackage{subcaption}\n\\usepackage{graphicx}\n\\usepackage[margin=0.8in, bottom=1.2in]{geometry}\n\\usepackage[page]{appendix}\n\\pagestyle{fancy}\n\\renewcommand{\\headrulewidth}{0pt}\n\\fancyhead{}\n\\rfoot{Page \\thepage\\  of \\pageref{LastPage}}\n\\cfoot{}\n\\begin{document}\n\\begin{table}\n\\centering\n\\begin{threeparttable}\n\\caption{My Table Title}\n\\begin{tabular}{lcc}\n\\toprule\na & b & c\\\\\n 1 &  2 &  3 \\\\\n 4 &  5 &  6 \\\\\n 7 &  8 &  9 \\\\\n\\bottomrule\n\n\\end{tabular}\n\\begin{tablenotes}[para, flushleft]\nMy below text\n\\end{tablenotes}\n\\end{threeparttable}\n\\end{table}\n\\end{document}'
        name = 'document with table'
        doc.to_pdf(outfolder=GENERATED_FILES_DIR, outname=name)
        compare_pdfs_in_generated_vs_input_by_name(name)

    def test_two_panel_table_in_document(self):
        doc = pl.Document([self.two_panel_table_from_lol_with_index])
        assert str(doc) == '\\documentclass[]{article}\n\\usepackage{threeparttable}\n\\usepackage{booktabs}\n\\usepackage{dcolumn}\n\\newcolumntype{L}[1]{>{\\raggedright\\let\\newline\\\\\\arraybackslash\\hspace{0pt}}m{#1}}\n\\newcolumntype{C}[1]{>{\\centering\\let\\newline\\\\\\arraybackslash\\hspace{0pt}}m{#1}}\n\\newcolumntype{R}[1]{>{\\raggedleft\\let\\newline\\\\\\arraybackslash\\hspace{0pt}}m{#1}}\n\\newcolumntype{.}{D{.}{.}{-1}}\n\\usepackage{amsmath}\n\\usepackage{pdflscape}\n\\usepackage{array}\n\\usepackage{fancyhdr}\n\\usepackage{lastpage}\n\\usepackage{textcomp}\n\\usepackage[T1]{fontenc}\n\\usepackage{caption}\n\\usepackage{subcaption}\n\\usepackage{graphicx}\n\\usepackage[margin=0.8in, bottom=1.2in]{geometry}\n\\usepackage[page]{appendix}\n\\pagestyle{fancy}\n\\renewcommand{\\headrulewidth}{0pt}\n\\fancyhead{}\n\\rfoot{Page \\thepage\\  of \\pageref{LastPage}}\n\\cfoot{}\n\\begin{document}\n\\begin{table}\n\\centering\n\\begin{threeparttable}\n\\caption{My Table Title}\n\\begin{tabular}{lccc}\n\\toprule\n  & a & b & c\\\\\n\\midrule\n\\multicolumn{4}{l}{Panel A: One}\\\\\n0 &  1 &  2 &  3 \\\\\n1 &  4 &  5 &  6 \\\\\n2 &  7 &  8 &  9 \\\\\n  &   &   &  \\\\\n\\multicolumn{4}{l}{Panel B: Two}\\\\\n0 &  11 &  12 &  13 \\\\\n1 &  14 &  15 &  16 \\\\\n2 &  17 &  18 &  19 \\\\\n\\bottomrule\n\n\\end{tabular}\n\\begin{tablenotes}[para, flushleft]\nMy below text\n\\end{tablenotes}\n\\end{threeparttable}\n\\end{table}\n\\end{document}'
        name = 'document with two panel table'
        doc.to_pdf(outfolder=GENERATED_FILES_DIR, outname=name)
        compare_pdfs_in_generated_vs_input_by_name(name)
