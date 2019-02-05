from dero.latex.models.section.base import SectionBase
from dero.latex.models.section.paragraphs import Paragraph


class SubSubSection(SectionBase):
    name = 'subsubsection'
    next_level_down_class = Paragraph


class SubSection(SectionBase):
    name = 'subsection'
    next_level_down_class = SubSubSection


class Section(SectionBase):
    name = 'section'
    next_level_down_class = SubSection





