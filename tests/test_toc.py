from pyexlatex import TableOfContents


def test_toc():
    assert str(TableOfContents()) == '\\tableofcontents'
    assert str(TableOfContents(options=('currentsection',))) == '\\tableofcontents[currentsection]'
