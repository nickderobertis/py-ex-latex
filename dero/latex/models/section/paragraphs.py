from dero.latex.models.section.base import ParagraphBase


class SubParagraph(ParagraphBase):
    name = 'subparagraph'


class Paragraph(ParagraphBase):
    name = 'paragraph'
    next_level_down_class = SubParagraph


