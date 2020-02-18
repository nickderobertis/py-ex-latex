from pyexlatex import BibTexArticle


def test_bibtex_eq():
    common_args = (
        'da-engelberg-gao-2011',
        'Zhi Da and Joseph Engelberg and Pengjie Gao',
        'In Search of Attention',
        'Journal of Finance',
        '2011',
    )

    common_kwargs = dict(
        volume='66',
        number='5',
        pages='1461-1499',
        month='10'
    )

    bto1 = BibTexArticle(*common_args, **common_kwargs)
    bto2 = BibTexArticle(*common_args, **common_kwargs)

    assert bto1 == bto2