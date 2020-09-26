from pyexlatex.models.blindtext import BlindText
from tests.base import NoOptionsNoContentsItemTest


class TestBlindText(NoOptionsNoContentsItemTest):
    item_class = BlindText
    tag_name = 'blindtext'
