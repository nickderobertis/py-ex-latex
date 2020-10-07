import pyexlatex as pl
from tests.base import EXAMPLE_IMAGE_PATH, GENERATED_FILES_DIR

EXPECT_GRAPHIC = '\\vcenteredinclude{width=0.1\\textwidth}{Sources/nd-logo.png}'


def test_inline_graphic():
    ig = pl.InlineGraphic(str(EXAMPLE_IMAGE_PATH), width=0.1)
    assert str(ig) == EXPECT_GRAPHIC


def test_inline_graphic_in_document():
    ig = pl.InlineGraphic(str(EXAMPLE_IMAGE_PATH), width=0.1)
    contents = ['Some inline text before', ig, 'and after and then wrapping onto the next line so that '
                                               'I can make sure that it is working properly in the case '
                                               'that it is used in a real document']
    doc = pl.Document(contents)
    assert r"""
\newcommand{\vcenteredinclude}[2]{\begingroup
\setbox0=\hbox{\includegraphics[#1]{#2}}%
\parbox{\wd0}{\box0}\endgroup}
    """.strip() in str(doc)
    assert EXPECT_GRAPHIC in str(doc)
