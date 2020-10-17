import pyexlatex as pl
from tests.base import EXAMPLE_IMAGE_PATH, GENERATED_FILES_DIR, INPUT_FILES_DIR
from tests.utils.pdf import compare_pdfs

EXPECT_GRAPHIC = '\\vcenteredinclude{width=0.1\\textwidth}{Sources/nd-logo.png}'
EXPECT_DEFINITION = r"""
\newcommand{\vcenteredinclude}[2]{\begingroup
\setbox0=\hbox{\includegraphics[#1]{#2}}%
\parbox{\wd0}{\box0}\endgroup}
    """.strip()


def test_inline_graphic():
    ig = pl.InlineGraphic(str(EXAMPLE_IMAGE_PATH), width=0.1)
    assert str(ig) == EXPECT_GRAPHIC


def test_inline_graphic_in_document():
    ig = pl.InlineGraphic(str(EXAMPLE_IMAGE_PATH), width=0.1)
    ig2 = pl.InlineGraphic(str(EXAMPLE_IMAGE_PATH), width=0.1)
    contents = ['Some inline text before', ig, 'and after and then wrapping onto the next line so that '
                                               'I can make sure that it is working properly in the case '
                                               'that it is used in a real document', ig2]
    doc = pl.Document(contents)
    assert EXPECT_DEFINITION in str(doc)
    assert EXPECT_GRAPHIC in str(doc)
    doc.to_pdf(GENERATED_FILES_DIR, outname='inline graphic document')
    compare_pdfs(INPUT_FILES_DIR / 'inline graphic document.pdf', GENERATED_FILES_DIR / 'inline graphic document.pdf')
