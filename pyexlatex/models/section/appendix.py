from pyexlatex.models.section.base import TextAreaBase
from pyexlatex.models.section.sections import Section


class Appendix(TextAreaBase):
    name = 'appendices'
    next_level_down_class = Section

    def __init__(self, contents):
        super().__init__(self.name, contents)
