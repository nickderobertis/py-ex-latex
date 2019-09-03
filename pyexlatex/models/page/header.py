from pyexlatex.models.item import SimpleItem, ItemBase
from pyexlatex.models.containeritem import ContainerItem
from pyexlatex.models.section.base import TextAreaMixin
from pyexlatex.logic.builder import _build


class RightHeader(TextAreaMixin, SimpleItem):
    name = 'rhead'

    def __init__(self, contents):
        super().__init__(self.name, contents)


class CenterHeader(TextAreaMixin, SimpleItem):
    name = 'chead'

    def __init__(self, contents):
        super().__init__(self.name, contents)


class LeftHeader(TextAreaMixin, SimpleItem):
    name = 'lhead'

    def __init__(self, contents):
        super().__init__(self.name, contents)


class Header(ContainerItem, ItemBase):
    """
    Adds a header to a document, aligned to right, center, or left.
    """

    def __init__(self, contents, align: str = 'right'):
        """

        :param contents:
        :param align: one of 'right', 'left', 'center'
        """
        self.align = align.lower()
        self.contents = self._get_positioned_header(contents)
        super().__init__(self.contents.name, self.contents)

    def _get_positioned_header(self, contents):
        if self.align == 'right':
            return RightHeader(contents)
        elif self.align == 'left':
            return LeftHeader(contents)
        elif self.align == 'center':
            return CenterHeader(contents)
        else:
            raise ValueError('must pass one of "right", "left", "center" for align')

    def __str__(self):
        return str(self.contents)


class FancyHeader(SimpleItem):
    name = 'fancyhead'

    def __init__(self, contents):
        super().__init__(self.name, contents)

remove_header_line = r'\renewcommand{\headrulewidth}{0pt}'
remove_header = _build([
    remove_header_line,
    FancyHeader('')  # remove header default contents
])