from typing import Optional
from pyexlatex.models.template import Template
from pyexlatex.models.format.text.bold import Bold
from pyexlatex.models.format.breaks import OutputLineBreak
from pyexlatex.layouts.spaced import HorizontallySpaced


class Award(Template):
    """
    Represents an award or grant in a resume.
    """
    SPACE_BETWEEN_ADJUSTMENT = '-14pt'

    def __init__(self, award_name: str, received: Optional[str] = None, extra_info: Optional[str] = None):
        self.award_name = award_name
        self.received = received
        self.extra_info = extra_info
        self.contents = self._get_contents()
        super().__init__()

    def _get_contents(self):
        items = [item for item in [self._award_obj, self.received] if item is not None]
        return [
            HorizontallySpaced(items),
            OutputLineBreak(size_adjustment=self.SPACE_BETWEEN_ADJUSTMENT)
        ]

    @property
    def _award_obj(self):
        if self.extra_info is None:
            return self._award_formatter(self.award_name)

        return [self._award_formatter(self.award_name), f' ({self.extra_info})']

    def _award_formatter(self, award_str: str):
        return Bold(award_str)
