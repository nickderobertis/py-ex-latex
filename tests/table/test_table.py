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


def test_table():
    table = pl.Table.from_list_of_lists_of_dfs(
        [[EXAMPLE_DF]],
        caption='My Table Title',
        below_text='My below text'
    )
    assert str(table) == '\\begin{table}\n\\centering\n\\begin{threeparttable}\n\\caption{My Table Title}\n\\begin{tabular}{lcc}\n\\toprule\na & b & c\\\\\n 1 &  2 &  3 \\\\\n 4 &  5 &  6 \\\\\n 7 &  8 &  9 \\\\\n\\bottomrule\n\n\\end{tabular}\n\\begin{tablenotes}[para, flushleft]\nMy below text\n\\end{tablenotes}\n\\end{threeparttable}\n\\end{table}'


def test_table_in_document():
    table = pl.Table.from_list_of_lists_of_dfs(
        [[EXAMPLE_DF]],
        caption='My Table Title',
        below_text='My below text'
    )
    doc = pl.Document([table])
    assert str(doc) == '\\documentclass[]{article}\n\\usepackage{threeparttable}\n\\usepackage{booktabs}\n\\usepackage{amsmath}\n\\usepackage{pdflscape}\n\\usepackage{array}\n\\usepackage{fancyhdr}\n\\usepackage{lastpage}\n\\usepackage{textcomp}\n\\usepackage{dcolumn}\n\\newcolumntype{L}[1]{>{\\raggedright\\let\\newline\\\\\\arraybackslash\\hspace{0pt}}m{#1}}\n\\newcolumntype{C}[1]{>{\\centering\\let\\newline\\\\\\arraybackslash\\hspace{0pt}}m{#1}}\n\\newcolumntype{R}[1]{>{\\raggedleft\\let\\newline\\\\\\arraybackslash\\hspace{0pt}}m{#1}}\n\\newcolumntype{.}{D{.}{.}{-1}}\n\\usepackage[T1]{fontenc}\n\\usepackage{caption}\n\\usepackage{subcaption}\n\\usepackage{graphicx}\n\\usepackage[margin=0.8in, bottom=1.2in]{geometry}\n\\usepackage[page]{appendix}\n\\pagestyle{fancy}\n\\renewcommand{\\headrulewidth}{0pt}\n\\fancyhead{}\n\\rfoot{Page \\thepage\\  of \\pageref{LastPage}}\n\\cfoot{}\n\\begin{document}\n\\begin{table}\n\\centering\n\\begin{threeparttable}\n\\caption{My Table Title}\n\\begin{tabular}{lcc}\n\\toprule\na & b & c\\\\\n 1 &  2 &  3 \\\\\n 4 &  5 &  6 \\\\\n 7 &  8 &  9 \\\\\n\\bottomrule\n\n\\end{tabular}\n\\begin{tablenotes}[para, flushleft]\nMy below text\n\\end{tablenotes}\n\\end{threeparttable}\n\\end{table}\n\\end{document}'
    name = 'document with table'
    doc.to_pdf(outfolder=GENERATED_FILES_DIR, outname=name)
    compare_pdfs_in_generated_vs_input_by_name(name)
