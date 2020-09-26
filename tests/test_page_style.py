from pyexlatex.models.page.footer import RightFooter
from pyexlatex.models.page.header import FancyHeader
from pyexlatex.models.page.style import PageStyle, ThisPageStyle, FancyPageStyle
from tests.base import SimpleItemTest, MultiOptionSimpleItemTest


class TestPageStyle(SimpleItemTest):
    item_class = PageStyle
    tag_name = 'pagestyle'


class TestThisPageStyle(SimpleItemTest):
    item_class = ThisPageStyle
    tag_name = 'thispagestyle'


class TestFancyPageStyle:

    def test_str(self):
        content = FancyPageStyle('woo')
        assert str(content) == '\\fancypagestyle{plain}{woo}'

    def test_list(self):
        content = FancyPageStyle(['woo', FancyHeader('stuff'), RightFooter('yeah')])
        assert str(content) == '\\fancypagestyle{plain}{woo\n\\fancyhead{stuff}\n\\rfoot{yeah}}'

