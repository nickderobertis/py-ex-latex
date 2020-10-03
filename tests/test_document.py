import datetime

import pyexlatex as pl
from pyexlatex import Package, LeftFooter, RightFooter, FooterLine, CenterFooter, ThisPageNumber
from pyexlatex.models.blindtext import BlindText
from pyexlatex.models.document import Document
from pyexlatex.models.page.number import PageReference
from pyexlatex.texgen.packages.default import default_packages
from tests.base import INPUT_FILES_DIR, GENERATED_FILES_DIR
from tests.utils.pdf import compare_pdfs


class TestDocument:
    no_options_result = '\\documentclass[]{article}\n\\usepackage{amsmath}\n\\usepackage{pdflscape}\n\\usepackage{booktabs}\n\\usepackage{array}\n\\usepackage{threeparttable}\n\\usepackage{fancyhdr}\n\\usepackage{lastpage}\n\\usepackage{textcomp}\n\\usepackage{dcolumn}\n\\newcolumntype{L}[1]{>{\\raggedright\\let\\newline\\\\\\arraybackslash\\hspace{0pt}}m{#1}}\n\\newcolumntype{C}[1]{>{\\centering\\let\\newline\\\\\\arraybackslash\\hspace{0pt}}m{#1}}\n\\newcolumntype{R}[1]{>{\\raggedleft\\let\\newline\\\\\\arraybackslash\\hspace{0pt}}m{#1}}\n\\newcolumntype{.}{D{.}{.}{-1}}\n\\usepackage[T1]{fontenc}\n\\usepackage{caption}\n\\usepackage{subcaption}\n\\usepackage{graphicx}\n\\usepackage[margin=0.8in, bottom=1.2in]{geometry}\n\\usepackage[page]{appendix}\n\\pagestyle{fancy}\n\\renewcommand{\\headrulewidth}{0pt}\n\\fancyhead{}\n\\rfoot{Page \\thepage\\  of \\pageref{LastPage}}\n\\cfoot{}\n\\begin{document}\nwoo\n\\end{document}'
    common_kwargs = dict(
        packages=default_packages + ['hyperref', Package('tikz')],
        landscape=False,  # TODO: set landscape to True in Document tests once landscape bug is fixed
        title='My Title',
        authors=['Person One', 'Human Two'],
        date=datetime.datetime(2020, 10, 1),
        abstract='Some text for the abstract',
        skip_title_page=False,
        page_modifier_str='margin=1in',
        page_header=True,
        page_numbers=False,
        appendix_modifier_str='page',
        section_numbering_styles=dict(
            section=r'\Roman{section}',
            subsection=r'\thesection.\Alph{subsection}',
            subsubsection=r'\thesubsection.\arabic{subsubsection}',
            subfigure=r'\roman{subfigure}',
        ),
        floats_at_end=True,
        floats_at_end_options='nolists',
        document_type='article',
        font_size=12,
        num_columns=2,
        line_spacing=2,
        tables_relative_font_size=-1,
        figures_relative_font_size=1,
        page_style='fancy',
        custom_headers=[
            pl.Header(pl.SmallCaps('short title'), align='left'),
            pl.Header(pl.SmallCaps(['Page ', pl.ThisPageNumber()]))
        ],
        remove_section_numbering=True,
        separate_abstract_page=True,
        extra_title_page_lines=[pl.Italics('Stuff:'), 'Yeah, things'],
        empty_title_page_style=False,
        pre_output_func=lambda x: x + '\n\n\n',
    )

    def test_no_options_str(self):
        doc = Document('woo')
        assert str(doc) == self.no_options_result

    def test_no_options_list(self):
        doc = Document(['woo'])
        assert str(doc) == self.no_options_result

    def test_basic_title_page(self):
        doc = Document([BlindText(), ''] * 10, authors=['Person One', 'Human Two', 'Being Three'], title='My Title')
        assert str(doc) == '\\documentclass[]{article}\n\\usepackage{blindtext}\n\\usepackage{amsmath}\n\\usepackage{pdflscape}\n\\usepackage{booktabs}\n\\usepackage{array}\n\\usepackage{threeparttable}\n\\usepackage{fancyhdr}\n\\usepackage{lastpage}\n\\usepackage{textcomp}\n\\usepackage{dcolumn}\n\\newcolumntype{L}[1]{>{\\raggedright\\let\\newline\\\\\\arraybackslash\\hspace{0pt}}m{#1}}\n\\newcolumntype{C}[1]{>{\\centering\\let\\newline\\\\\\arraybackslash\\hspace{0pt}}m{#1}}\n\\newcolumntype{R}[1]{>{\\raggedleft\\let\\newline\\\\\\arraybackslash\\hspace{0pt}}m{#1}}\n\\newcolumntype{.}{D{.}{.}{-1}}\n\\usepackage[T1]{fontenc}\n\\usepackage{caption}\n\\usepackage{subcaption}\n\\usepackage{graphicx}\n\\usepackage[margin=0.8in, bottom=1.2in]{geometry}\n\\usepackage[page]{appendix}\n\\pagestyle{fancy}\n\\renewcommand{\\headrulewidth}{0pt}\n\\fancyhead{}\n\\rfoot{Page \\thepage\\  of \\pageref{LastPage}}\n\\cfoot{}\n\\begin{document}\n\\title{My Title}\n\\author{Person One, Human Two, and Being Three}\n\\date{\\today}\n\\maketitle\n\\blindtext\n\n\\blindtext\n\n\\blindtext\n\n\\blindtext\n\n\\blindtext\n\n\\blindtext\n\n\\blindtext\n\n\\blindtext\n\n\\blindtext\n\n\\blindtext\n\n\\end{document}'

    def test_title_page_with_consistent_formatting(self):
        doc = Document([BlindText(), ''] * 10, authors=['Person One', 'Human Two', 'Being Three'], title='My Title', apply_page_style_to_section_starts=True)
        assert str(doc) == '\\documentclass[]{article}\n\\usepackage{blindtext}\n\\usepackage{amsmath}\n\\usepackage{pdflscape}\n\\usepackage{booktabs}\n\\usepackage{array}\n\\usepackage{threeparttable}\n\\usepackage{fancyhdr}\n\\usepackage{lastpage}\n\\usepackage{textcomp}\n\\usepackage{dcolumn}\n\\newcolumntype{L}[1]{>{\\raggedright\\let\\newline\\\\\\arraybackslash\\hspace{0pt}}m{#1}}\n\\newcolumntype{C}[1]{>{\\centering\\let\\newline\\\\\\arraybackslash\\hspace{0pt}}m{#1}}\n\\newcolumntype{R}[1]{>{\\raggedleft\\let\\newline\\\\\\arraybackslash\\hspace{0pt}}m{#1}}\n\\newcolumntype{.}{D{.}{.}{-1}}\n\\usepackage[T1]{fontenc}\n\\usepackage{caption}\n\\usepackage{subcaption}\n\\usepackage{graphicx}\n\\usepackage[margin=0.8in, bottom=1.2in]{geometry}\n\\usepackage[page]{appendix}\n\\pagestyle{fancy}\n\\renewcommand{\\headrulewidth}{0pt}\n\\fancyhead{}\n\\rfoot{Page \\thepage\\  of \\pageref{LastPage}}\n\\cfoot{}\n\\fancypagestyle{plain}{\\rfoot{Page \\thepage\\  of \\pageref{LastPage}}\n\\cfoot{}}\n\\begin{document}\n\\title{My Title}\n\\author{Person One, Human Two, and Being Three}\n\\date{\\today}\n\\maketitle\n\\blindtext\n\n\\blindtext\n\n\\blindtext\n\n\\blindtext\n\n\\blindtext\n\n\\blindtext\n\n\\blindtext\n\n\\blindtext\n\n\\blindtext\n\n\\blindtext\n\n\\end{document}'

    def test_custom_footer(self):
        doc = Document(
            'woo',
            custom_footers=[
                LeftFooter('stuff'),
                CenterFooter(''),
                RightFooter(
                    ['Page', ThisPageNumber(), '\\', 'of', PageReference('LastPage')]
                ),
                FooterLine()
            ]
        )
        assert str(doc) == '\\documentclass[]{article}\n\\usepackage{amsmath}\n\\usepackage{pdflscape}\n\\usepackage{booktabs}\n\\usepackage{array}\n\\usepackage{threeparttable}\n\\usepackage{fancyhdr}\n\\usepackage{lastpage}\n\\usepackage{textcomp}\n\\usepackage{dcolumn}\n\\newcolumntype{L}[1]{>{\\raggedright\\let\\newline\\\\\\arraybackslash\\hspace{0pt}}m{#1}}\n\\newcolumntype{C}[1]{>{\\centering\\let\\newline\\\\\\arraybackslash\\hspace{0pt}}m{#1}}\n\\newcolumntype{R}[1]{>{\\raggedleft\\let\\newline\\\\\\arraybackslash\\hspace{0pt}}m{#1}}\n\\newcolumntype{.}{D{.}{.}{-1}}\n\\usepackage[T1]{fontenc}\n\\usepackage{caption}\n\\usepackage{subcaption}\n\\usepackage{graphicx}\n\\usepackage[margin=0.8in, bottom=1.2in]{geometry}\n\\usepackage[page]{appendix}\n\\pagestyle{fancy}\n\\renewcommand{\\headrulewidth}{0pt}\n\\fancyhead{}\n\\lfoot{stuff}\n\\cfoot{}\n\\rfoot{Page\n\\thepage\n\\\nof\n\\pageref{LastPage}}\n\\renewcommand{\\footrulewidth}{0.4pt}\n\\begin{document}\nwoo\n\\end{document}'

    def test_all_options_with_title_page(self):
        doc = Document(
            'woo',
            **self.common_kwargs,
        )

        assert str(doc) == '\\documentclass[12pt, twocolumn]{article}\n\\usepackage{amsmath}\n\\usepackage{pdflscape}\n\\usepackage{booktabs}\n\\usepackage{array}\n\\usepackage{threeparttable}\n\\usepackage{fancyhdr}\n\\usepackage{lastpage}\n\\usepackage{textcomp}\n\\usepackage{dcolumn}\n\\newcolumntype{L}[1]{>{\\raggedright\\let\\newline\\\\\\arraybackslash\\hspace{0pt}}m{#1}}\n\\newcolumntype{C}[1]{>{\\centering\\let\\newline\\\\\\arraybackslash\\hspace{0pt}}m{#1}}\n\\newcolumntype{R}[1]{>{\\raggedleft\\let\\newline\\\\\\arraybackslash\\hspace{0pt}}m{#1}}\n\\newcolumntype{.}{D{.}{.}{-1}}\n\\usepackage[T1]{fontenc}\n\\usepackage{caption}\n\\usepackage{subcaption}\n\\usepackage{graphicx}\n\\usepackage{hyperref}\n\\usepackage{tikz}\n\\usepackage[margin=1in]{geometry}\n\\usepackage{floatrow}\n\\DeclareFloatFont{small}{\\small}\n\\floatsetup[table]{font=small,capposition=top}\n\\DeclareFloatFont{large}{\\large}\n\\floatsetup[figure]{font=large,capposition=top}\n\\usepackage[nolists]{endfloat}\n\\DeclareDelayedFloatFlavor{ltable}{table}\n\\DeclareDelayedFloatFlavor{lfigure}{figure}\n\\usepackage{setspace}\n\\doublespacing\n\\usepackage[page]{appendix}\n\\renewcommand{\\thesection}{\\Roman{section}}\n\\renewcommand{\\thesubsection}{\\thesection.\\Alph{subsection}}\n\\renewcommand{\\thesubsubsection}{\\thesubsection.\\arabic{subsubsection}}\n\\renewcommand{\\thesubfigure}{\\roman{subfigure}}\n\\setcounter{secnumdepth}{0}\n\\pagestyle{fancy}\n\\lhead{\\textsc{short title}}\n\\rhead{\\textsc{Page \n\\thepage}}\n\\cfoot{}\n\\begin{document}\n\\title{My Title}\n\\author{Person One and Human Two}\n\\date{2020-10-01 00:00:00}\n\\maketitle\n\\newpage\n\\thispagestyle{empty}\n{\n\\begin{center}\n\\setlength{\\baselineskip}{40pt}\n\\LARGE\n\\textbf{My Title}\n\\end{center}\n}\n\\vspace{35pt}\n\\begin{center}\n\\textbf{Abstract}\n\\end{center}\n\\vspace{-10pt}\n\\hspace{1.5em}\nSome text for the abstract\n\\vspace{20pt}\n\\textit{Stuff:}\n\n\nYeah, things\n\n\n\\newpage\n\\setcounter{page}{1}\nwoo\n\n\n\n\\end{document}'

    def test_all_options_no_title_page(self):
        kwargs = {**self.common_kwargs}
        kwargs['skip_title_page'] = True

        doc = Document(
            'woo',
            **kwargs
        )

        assert str(doc) == '\\documentclass[12pt, twocolumn]{article}\n\\usepackage{amsmath}\n\\usepackage{pdflscape}\n\\usepackage{booktabs}\n\\usepackage{array}\n\\usepackage{threeparttable}\n\\usepackage{fancyhdr}\n\\usepackage{lastpage}\n\\usepackage{textcomp}\n\\usepackage{dcolumn}\n\\newcolumntype{L}[1]{>{\\raggedright\\let\\newline\\\\\\arraybackslash\\hspace{0pt}}m{#1}}\n\\newcolumntype{C}[1]{>{\\centering\\let\\newline\\\\\\arraybackslash\\hspace{0pt}}m{#1}}\n\\newcolumntype{R}[1]{>{\\raggedleft\\let\\newline\\\\\\arraybackslash\\hspace{0pt}}m{#1}}\n\\newcolumntype{.}{D{.}{.}{-1}}\n\\usepackage[T1]{fontenc}\n\\usepackage{caption}\n\\usepackage{subcaption}\n\\usepackage{graphicx}\n\\usepackage{hyperref}\n\\usepackage{tikz}\n\\usepackage[margin=1in]{geometry}\n\\usepackage{floatrow}\n\\DeclareFloatFont{small}{\\small}\n\\floatsetup[table]{font=small,capposition=top}\n\\DeclareFloatFont{large}{\\large}\n\\floatsetup[figure]{font=large,capposition=top}\n\\usepackage[nolists]{endfloat}\n\\DeclareDelayedFloatFlavor{ltable}{table}\n\\DeclareDelayedFloatFlavor{lfigure}{figure}\n\\usepackage{setspace}\n\\doublespacing\n\\usepackage[page]{appendix}\n\\renewcommand{\\thesection}{\\Roman{section}}\n\\renewcommand{\\thesubsection}{\\thesection.\\Alph{subsection}}\n\\renewcommand{\\thesubsubsection}{\\thesubsection.\\arabic{subsubsection}}\n\\renewcommand{\\thesubfigure}{\\roman{subfigure}}\n\\setcounter{secnumdepth}{0}\n\\pagestyle{fancy}\n\\lhead{\\textsc{short title}}\n\\rhead{\\textsc{Page \n\\thepage}}\n\\cfoot{}\n\\begin{document}\nwoo\n\n\n\n\\end{document}'

    def test_to_pdf(self):
        doc = Document('woo')
        doc.to_pdf(GENERATED_FILES_DIR)
        compare_pdfs(INPUT_FILES_DIR / 'document.pdf', GENERATED_FILES_DIR / 'document.pdf')

    def test_to_html(self):
        doc = Document('woo')
        doc.to_html(GENERATED_FILES_DIR)
        expect_str = (INPUT_FILES_DIR / 'document.html').read_text()
        generated_str = (GENERATED_FILES_DIR / 'document.html').read_text()
        assert _remove_meta_tags(expect_str) == _remove_meta_tags(generated_str)


def _remove_meta_tags(content: str) -> str:
    lines = content.splitlines()
    out_str = ''
    for line in lines:
        if line.startswith('<meta'):
            continue
        else:
            out_str += line
            out_str += '\n'
    return out_str
