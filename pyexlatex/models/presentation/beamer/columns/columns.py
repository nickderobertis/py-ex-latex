from pyexlatex.models.section.base import TextAreaBase


class Columns(TextAreaBase):
    name = 'columns'
    repr_cols = ['contents']

    def __init__(self, content, **kwargs):
        super().__init__(self.name, content, **kwargs)
