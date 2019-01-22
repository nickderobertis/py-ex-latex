from dero.latex.models.section.base import SectionBase


class Section(SectionBase):
    name = 'section'


class SubSection(SectionBase):
    name = 'subsection'


class SubSubSection(SectionBase):
    name = 'subsubsection'