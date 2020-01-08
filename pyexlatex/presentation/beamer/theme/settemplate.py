from pyexlatex.models.item import MultiOptionSimpleItem
from pyexlatex.models.section.base import TextAreaMixin


class SetBeamerTemplate(TextAreaMixin, MultiOptionSimpleItem):
    name = 'setbeamertemplate'

    def __init__(self, beamer_item: str, content, **kwargs):
        TextAreaMixin.__init__(self, self.name, content)
        MultiOptionSimpleItem.__init__(self, self.name, beamer_item, self.contents, **kwargs)
