import pandas as pd

import pyexlatex as pl

from tests.base import GENERATED_FILES_DIR, EXAMPLE_IMAGE_PATH
from tests.utils.pdf import compare_pdfs_in_generated_vs_input_by_name


def test_basic_presentation():
    doc = pl.Presentation(['woo'])
    assert str(doc) == '\\documentclass[11pt]{beamer}\n\\mode\n<presentation>{\\usetheme{Madrid}}\n\\begin{document}\nwoo\n\\end{document}'
    name = 'basic presentation'
    doc.to_pdf(outfolder=GENERATED_FILES_DIR, outname=name)
    compare_pdfs_in_generated_vs_input_by_name(name)


def test_presentation_options():
    doc = pl.Presentation(
        [
            pl.Section(
                [
                    pl.Frame(
                        [
                            'woo'
                        ],
                        title='One-One'
                    ),
                    pl.Frame(
                        [
                            'woo2'
                        ],
                        title='One-Two'
                    )
                ],
                title="One"
            ),
            pl.Section(
                [
                    pl.Frame(
                        [
                            'woo3'
                        ],
                        title='Two-One'
                    ),
                    pl.Frame(
                        [
                            'woo4'
                        ],
                        title='Two-Two'
                    )
                ],
                title="Two"
            )
        ],
        packages=['hyperref'],
        title='Test Presentation',
        authors=['Nick DeRobertis', 'Someone Else'],
        date='2020-10-19',
        short_title='Pres',
        subtitle='A Presentation for Testing Purposes',
        short_author='People',
        institutions=[['University of Florida', 'Line two'], ['Virginia Commonwealth University']],
        short_institution='UF & VCU',
        font_size=15,
        nav_header=True,
        toc_sections=True,
    )
    assert str(doc) == '\\documentclass[15pt]{beamer}\n\\mode\n<presentation>{\\usetheme{Madrid}}\n\\institute[UF \\& VCU]{\\inst{1}\nUniversity of Florida\\\\\nLine two\n\\and\n\\inst{2}\nVirginia Commonwealth University}\n\\setbeamertemplate{headline}{\\begin{beamercolorbox}[ht=2.25ex, dp=3.75ex]{section in head/foot}\n\\insertnavigation{\\paperwidth}\n\\end{beamercolorbox}}\n\\AtBeginSection{\\begin{frame}\n\\frametitle{Table of Contents}\n\\tableofcontents[currentsection]\n\\end{frame}}\n\\begin{document}\n\\title[Pres]{Test Presentation}\n\\subtitle{A Presentation for Testing Purposes}\n\\author[People]{Nick DeRobertis\\inst{1}, Someone Else\\inst{2}}\n\\date{2020-10-19}\n\\begin{frame}\n\\titlepage\n\\label{title-frame}\n\\end{frame}\n\\begin{section}{One}\n\\begin{frame}\n\\frametitle{One-One}\nwoo\n\\end{frame}\n\\begin{frame}\n\\frametitle{One-Two}\nwoo2\n\\end{frame}\n\\end{section}\n\\begin{section}{Two}\n\\begin{frame}\n\\frametitle{Two-One}\nwoo3\n\\end{frame}\n\\begin{frame}\n\\frametitle{Two-Two}\nwoo4\n\\end{frame}\n\\end{section}\n\\end{document}'
    name = 'presentation with options'
    doc.to_pdf(outfolder=GENERATED_FILES_DIR, outname=name)
    compare_pdfs_in_generated_vs_input_by_name(name)


def test_table_in_presentation():
    df = pd.DataFrame(
        [
            (1, 2, 3.546),
            (4, 5, 66546.4),
            (7, 8, 96.54)
        ],
        columns=['a', 'b', 'c']
    )
    table = pl.Table.from_list_of_lists_of_dfs(
        [[df]],
        caption='My Table Title',
        below_text='My below text',
        align='L{5cm}c.',
        mid_rules=False,
    )
    doc = pl.Presentation(
        [
            pl.Section(
                [
                    pl.Frame(
                        [
                            table
                        ],
                        title='Table'
                    ),
                ],
                title="Section"
            ),
        ],
    )
    assert str(doc) == '\\documentclass[11pt]{beamer}\n\\mode\n<presentation>{\\usetheme{Madrid}}\n\\usepackage{threeparttable}\n\\usepackage{booktabs}\n\\usepackage{dcolumn}\n\\newcolumntype{L}[1]{>{\\raggedright\\let\\newline\\\\\\arraybackslash\\hspace{0pt}}m{#1}}\n\\newcolumntype{C}[1]{>{\\centering\\let\\newline\\\\\\arraybackslash\\hspace{0pt}}m{#1}}\n\\newcolumntype{R}[1]{>{\\raggedleft\\let\\newline\\\\\\arraybackslash\\hspace{0pt}}m{#1}}\n\\newcolumntype{.}{D{.}{.}{-1}}\n\\begin{document}\n\\begin{section}{Section}\n\\begin{frame}\n\\frametitle{Table}\n\\begin{table}\n\\centering\n\\begin{threeparttable}\n\\caption{My Table Title}\n\\begin{tabular}{L{5cm}c.}\n\\toprule\na & b & c\\\\\n 1 &  2 &      3.546 \\\\\n 4 &  5 &  66546.400 \\\\\n 7 &  8 &     96.540 \\\\\n\\bottomrule\n\n\\end{tabular}\n\\begin{tablenotes}[para, flushleft]\nMy below text\n\\end{tablenotes}\n\\end{threeparttable}\n\\end{table}\n\\end{frame}\n\\end{section}\n\\end{document}'
    name = 'presentation with table'
    doc.to_pdf(outfolder=GENERATED_FILES_DIR, outname=name)
    compare_pdfs_in_generated_vs_input_by_name(name)


def test_tabular_from_table_in_presentation():
    df = pd.DataFrame(
        [
            (1, 2, 3.546),
            (4, 5, 66546.4),
            (7, 8, 96.54)
        ],
        columns=['a', 'b', 'c']
    )
    table = pl.Table.from_list_of_lists_of_dfs(
        [[df], [df + 10]],
        caption='My Table Title',
        below_text='My below text',
        align='L{5cm}c.'
    )
    doc = pl.Presentation(
        [
            pl.Section(
                [
                    pl.Frame(
                        [
                            table.tex_obj(as_document=False, as_single_tabular=True),
                        ],
                        title='Tabular'
                    ),
                ],
                title="Section"
            ),
        ],
    )
    assert str(doc) == '\\documentclass[11pt]{beamer}\n\\mode\n<presentation>{\\usetheme{Madrid}}\n\\usepackage{booktabs}\n\\usepackage{dcolumn}\n\\newcolumntype{L}[1]{>{\\raggedright\\let\\newline\\\\\\arraybackslash\\hspace{0pt}}m{#1}}\n\\newcolumntype{C}[1]{>{\\centering\\let\\newline\\\\\\arraybackslash\\hspace{0pt}}m{#1}}\n\\newcolumntype{R}[1]{>{\\raggedleft\\let\\newline\\\\\\arraybackslash\\hspace{0pt}}m{#1}}\n\\newcolumntype{.}{D{.}{.}{-1}}\n\\begin{document}\n\\begin{section}{Section}\n\\begin{frame}\n\\frametitle{Tabular}\n\\begin{tabular}{L{5cm}c.}\n\\toprule\na & b & c\\\\\n\\midrule\n 1 &  2 &      3.546 \\\\\n 4 &  5 &  66546.400 \\\\\n 7 &  8 &     96.540 \\\\\n  &   &  \\\\\n 11 &  12 &     13.546 \\\\\n 14 &  15 &  66556.400 \\\\\n 17 &  18 &    106.540 \\\\\n\\bottomrule\n\n\\end{tabular}\n\\end{frame}\n\\end{section}\n\\end{document}'
    name = 'presentation with tabular'
    doc.to_pdf(outfolder=GENERATED_FILES_DIR, outname=name)
    compare_pdfs_in_generated_vs_input_by_name(name)


def test_tabular_list_from_table_in_presentation():
    df = pd.DataFrame(
        [
            (1, 2, 3.546),
            (4, 5, 66546.4),
            (7, 8, 96.54)
        ],
        columns=['a', 'b', 'c']
    )
    table = pl.Table.from_list_of_lists_of_dfs(
        [[df], [df + 10]],
        caption='My Table Title',
        below_text='My below text',
        align='L{5cm}c.'
    )
    frames = [
        pl.Frame(tab, title=f'Tabular {i + 1}')
        for i, tab in enumerate(table.tex_obj(as_document=False, as_panel_tabular_list=True))
    ]

    doc = pl.Presentation(
        [
            pl.Section(
                [
                    frames,
                ],
                title="Section"
            ),
        ],
    )
    assert str(doc) == '\\documentclass[11pt]{beamer}\n\\mode\n<presentation>{\\usetheme{Madrid}}\n\\usepackage{booktabs}\n\\usepackage{dcolumn}\n\\newcolumntype{L}[1]{>{\\raggedright\\let\\newline\\\\\\arraybackslash\\hspace{0pt}}m{#1}}\n\\newcolumntype{C}[1]{>{\\centering\\let\\newline\\\\\\arraybackslash\\hspace{0pt}}m{#1}}\n\\newcolumntype{R}[1]{>{\\raggedleft\\let\\newline\\\\\\arraybackslash\\hspace{0pt}}m{#1}}\n\\newcolumntype{.}{D{.}{.}{-1}}\n\\begin{document}\n\\begin{section}{Section}\n\\begin{frame}\n\\frametitle{Tabular 1}\n\\begin{tabular}{L{5cm}c.}\n\\toprule\na & b & c\\\\\n\\midrule\n 1 &  2 &      3.546 \\\\\n 4 &  5 &  66546.400 \\\\\n 7 &  8 &     96.540 \\\\\n\\bottomrule\n\n\\end{tabular}\n\\end{frame}\n\\begin{frame}\n\\frametitle{Tabular 2}\n\\begin{tabular}{L{5cm}c.}\n\\toprule\na & b & c\\\\\n\\midrule\n 11 &  12 &     13.546 \\\\\n 14 &  15 &  66556.400 \\\\\n 17 &  18 &    106.540 \\\\\n\\bottomrule\n\n\\end{tabular}\n\\end{frame}\n\\end{section}\n\\end{document}'
    name = 'presentation with tabular list'
    doc.to_pdf(outfolder=GENERATED_FILES_DIR, outname=name)
    compare_pdfs_in_generated_vs_input_by_name(name)


def test_figure_in_presentation():
    graphic = pl.Graphic(str(EXAMPLE_IMAGE_PATH), width=0.4)
    fig = pl.Figure([graphic], caption='My Figure')
    doc = pl.Presentation(
        [
            pl.Section(
                [
                    pl.Frame(
                        [
                            fig
                        ],
                        title='Figure'
                    ),
                ],
                title="Section"
            ),
        ],
    )
    assert str(doc) == '\\documentclass[11pt]{beamer}\n\\mode\n<presentation>{\\usetheme{Madrid}}\n\\begin{document}\n\\begin{section}{Section}\n\\begin{frame}\n\\frametitle{Figure}\n\\begin{figure}\n\\includegraphics[width=0.4\\textwidth]{Sources/nd-logo.png}\n\\caption{My Figure}\n\\end{figure}\n\\end{frame}\n\\end{section}\n\\end{document}'
    name = 'presentation with figure'
    doc.to_pdf(outfolder=GENERATED_FILES_DIR, outname=name)
    compare_pdfs_in_generated_vs_input_by_name(name)


def test_graphic_from_figure_in_presentation():
    graphic = pl.Graphic(str(EXAMPLE_IMAGE_PATH), width=0.4)
    fig = pl.Figure([graphic], caption='My Figure')
    doc = pl.Presentation(
        [
            pl.Section(
                [
                    pl.Frame(
                        [
                            fig.to_graphic_list()[0]
                        ],
                        title='Graphic'
                    ),
                ],
                title="Section"
            ),
        ],
    )
    assert str(doc) == '\\documentclass[11pt]{beamer}\n\\mode\n<presentation>{\\usetheme{Madrid}}\n\\begin{document}\n\\begin{section}{Section}\n\\begin{frame}\n\\frametitle{Graphic}\n\\includegraphics[width=0.4\\textwidth]{Sources/nd-logo.png}\n\\end{frame}\n\\end{section}\n\\end{document}'
    name = 'presentation with graphic from figure'
    doc.to_pdf(outfolder=GENERATED_FILES_DIR, outname=name)
    compare_pdfs_in_generated_vs_input_by_name(name)