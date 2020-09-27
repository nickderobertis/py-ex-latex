from pyexlatex import Document
from pyexlatex.models.format.captionsetup import CaptionSetup


def test_caption_setup_no_options():
    content = CaptionSetup()
    assert str(content) == '\\captionsetup[figure]{}'


def test_caption_setup_options():
    content = CaptionSetup(
        'table', relative_sizes={'font': -1, 'labelfont': 1}, options=['format=plain', 'indentation=.5cm']
    )
    assert str(content) == '\\captionsetup[table]{format=plain,indentation=.5cm,font=small,labelfont=large}'


def test_caption_in_document():
    content = CaptionSetup()
    doc = Document(['woo'], extra_pre_env_contents=[content])
    assert '\\captionsetup[figure]{}' in str(doc)
    assert '\\usepackage{caption}' in str(doc)

