from typing import Sequence

from pyexlatex.models.template import Template
from pyexlatex.models.item import SimpleItem
from pyexlatex.models.sizes.paperwidth import PaperWidth
from pyexlatex.presentation.beamer.colorbox import BeamerColorBox
from pyexlatex.presentation.beamer.theme.settemplate import SetBeamerTemplate


class InsertNavigation(SimpleItem):
    name = 'insertnavigation'

    def __init__(self, width, **kwargs):
        self.width = width
        super().__init__(self.name, width, **kwargs)


class AddNavigationHeader(Template):

    def __init__(self, options: Sequence[str] = ('ht=2.25ex', 'dp=3.75ex')):
        insert_nav = InsertNavigation(PaperWidth())
        color_box = BeamerColorBox(insert_nav, 'section in head/foot', options=options)
        set_template = SetBeamerTemplate('headline', color_box)
        self.contents = set_template
        super().__init__()
