import pytest
from pyexlatex import ColumnAlignment, ColumnsAlignment, Package


def test_column_align():
    assert str(ColumnAlignment("l")) == "l"
    assert str(ColumnAlignment("r")) == "r"
    assert str(ColumnAlignment("c")) == "c"
    assert str(ColumnAlignment(".")) == "."
    assert str(ColumnAlignment("L{2cm}")) == "L{2cm}"
    assert str(ColumnAlignment("R{2cm}")) == "R{2cm}"
    assert str(ColumnAlignment("C{2cm}")) == "C{2cm}"
    assert str(ColumnAlignment("d{2.5}")) == "d{2.5}"
    assert str(ColumnAlignment("D{.}{.}{2.5}")) == "D{.}{.}{2.5}"
    assert str(ColumnAlignment("s")) == "s"
    assert str(ColumnAlignment("S")) == "S"
    assert str(ColumnAlignment("|")) == "|"
    assert str(ColumnAlignment("@{}")) == "@{}"
    assert str(ColumnAlignment(r"@{\hspace{5cm}}")) == r"@{\hspace{5cm}}"
    assert str(ColumnAlignment("!{}")) == "!{}"
    assert str(ColumnAlignment(r"!{\hspace{5cm}}")) == r"!{\hspace{5cm}}"
    assert (
        str(ColumnAlignment("s[table-column-width=2cm]")) == "s[table-column-width=2cm]"
    )
    assert (
        str(ColumnAlignment("S[table-column-width=2cm]")) == "S[table-column-width=2cm]"
    )

    for bad_aligns in ['z', 'D{}', 'd{']:
        with pytest.raises(ValueError) as exc_info:
            ColumnAlignment("z")
        assert "expected alignment of" in str(exc_info.value)


def test_columns_align():
    align = ColumnsAlignment([ColumnAlignment("l"), ColumnAlignment("r")])
    assert str(align) == "lr"
    assert not align.data.packages

    align = ColumnsAlignment([ColumnAlignment("L{3cm}"), ColumnAlignment("R{3cm}")])
    assert str(align) == "L{3cm}R{3cm}"
    assert Package("dcolumn") in align.data.packages
    assert len(align.data.packages) == 1

    align = ColumnsAlignment(
        [ColumnAlignment("s[table-column-width=2cm]"), ColumnAlignment("S")]
    )
    assert str(align) == "s[table-column-width=2cm]S"
    assert Package("siunitx") in align.data.packages
    assert len(align.data.packages) == 1

    align = ColumnsAlignment([ColumnAlignment("L{3cm}"), ColumnAlignment("S")])
    assert str(align) == "L{3cm}S"
    assert Package("dcolumn") in align.data.packages
    assert Package("siunitx") in align.data.packages
    assert len(align.data.packages) == 2


def test_column_aligns_from_str():
    align_str = r"lc|r!{\hspace{2cm}}"
    align = ColumnsAlignment.from_alignment_str(align_str, num_columns=3)
    assert str(align) == align_str
    assert not align.data.packages

    align_str = "@{}lrcL{2cm}R{2cm}C{2cm}.s[table-column-width=2cm]S@{}rl@{}@{}c!{}"
    align = ColumnsAlignment.from_alignment_str(align_str, num_columns=12)
    assert str(align) == align_str
    assert Package("dcolumn") in align.data.packages
    assert Package("siunitx") in align.data.packages
    assert len(align.data.packages) == 2

    align_str = "L{5cm}@{}.@{}D{.}{.}{3.2}d{4.5}"
    align = ColumnsAlignment.from_alignment_str(align_str, num_columns=4)
    assert str(align) == align_str
    assert Package("dcolumn") in align.data.packages
    assert len(align.data.packages) == 1
