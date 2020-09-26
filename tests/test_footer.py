from pyexlatex.models.page.footer import LeftFooter, RightFooter, CenterFooter, FooterLine
from tests.base import SimpleItemTest


class TestLeftFooter(SimpleItemTest):
    item_class = LeftFooter
    tag_name = 'lfoot'


class TestRightFooter(SimpleItemTest):
    item_class = RightFooter
    tag_name = 'rfoot'


class TestCenterFooter(SimpleItemTest):
    item_class = CenterFooter
    tag_name = 'cfoot'


class TestFooterLine:

    def test_no_args(self):
        contents = FooterLine()
        assert str(contents) == '\\renewcommand{\\footrulewidth}{0.4pt}'

    def test_args(self):
        contents = FooterLine(1, 'cm')
        assert str(contents) == '\\renewcommand{\\footrulewidth}{1cm}'
