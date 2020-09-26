from pyexlatex.models.item import SimpleItem, MultiOptionSimpleItem
from pyexlatex.models.section.base import TextAreaMixin
from pyexlatex.typing import PyexlatexItems


class PageStyle(SimpleItem):
    """
    Sets style of the pages for the entire document.
    """
    name = 'pagestyle'

    def __init__(self, contents: PyexlatexItems):
        super().__init__(self.name, contents)


class ThisPageStyle(SimpleItem):
    """
    Sets style of the current page in a document.
    """
    name = 'thispagestyle'

    def __init__(self, contents: PyexlatexItems):
        super().__init__(self.name, contents)


class FancyPageStyle(TextAreaMixin, MultiOptionSimpleItem):
    """
    Redefines an existing page style such as plain but with fancy page style features.
    """
    name = 'fancypagestyle'

    def __init__(self, contents: PyexlatexItems, page_style: str = 'plain'):
        TextAreaMixin.__init__(self, self.name, contents)
        str_contents = self._build(self.contents)
        MultiOptionSimpleItem.__init__(self, self.name, page_style, str_contents)
