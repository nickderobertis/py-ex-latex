import pyexlatex as pl
from tests.base import GENERATED_FILES_DIR
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