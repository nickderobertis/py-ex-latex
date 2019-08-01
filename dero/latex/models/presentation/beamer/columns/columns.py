from dero.latex.models.section.base import TextAreaBase


class Columns(TextAreaBase):
    name = 'columns'

    def __init__(self, content, **kwargs):
        super().__init__(self.name, content, **kwargs)
