from typing import Optional
from pyexlatex.models.template import Template
from pyexlatex.models.format.text.bold import Bold
from pyexlatex.models.format.breaks import OutputLineBreak
from pyexlatex.layouts.spaced import HorizontallySpaced


class Award(Template):

    def __init__(self, award_name: str, received: Optional[str] = None):
        self.award_name = award_name
        self.received = received
        self.contents = self._get_contents()
        super().__init__()

    def _get_contents(self):
        items = [item for item in [self.award_name, self.received] if item is not None]
        items[0] = Bold(items[0])
        return [
            HorizontallySpaced(items),
            OutputLineBreak(size_adjustment='-14pt')
        ]
