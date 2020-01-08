from pyexlatex.models.section.base import SectionBase
from pyexlatex.models.section.paragraphs import Paragraph


class SubSubSection(SectionBase):
    """
    A part of a subsection, the third largest section type.
    """
    name = 'subsubsection'
    next_level_down_class = Paragraph


class SubSection(SectionBase):
    """
    A part of a section, the second largest section type.
    """
    name = 'subsection'
    next_level_down_class = SubSubSection


class Section(SectionBase):
    """
    A section of the document, the largest section type.
    """
    name = 'section'
    next_level_down_class = SubSection





