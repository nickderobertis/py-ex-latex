import pyexlatex as pl


def test_text_bold():
    text = 'woo'
    bold = pl.Bold(text)
    assert str(bold) == r'\textbf{woo}'
