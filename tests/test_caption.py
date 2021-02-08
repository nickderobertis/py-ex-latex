from pyexlatex.models.caption import Caption
from tests.base import SimpleItemTest


class TestCaption(SimpleItemTest):
    item_class = Caption
    tag_name = "caption"


def test_short_caption():
    capt = Caption("woo yeah", short_caption="woo")
    assert str(capt) == "\\caption[woo]{woo yeah}"
