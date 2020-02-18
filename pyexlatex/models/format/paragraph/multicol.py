from pyexlatex.models.section.base import TextAreaBase


class MultiColumn(TextAreaBase):
    """
    Layout multiple columns in a text area
    """
    name = 'multicols'

    def __init__(self, content, num_cols: int = 2, **kwargs):
        self.num_cols = num_cols
        self.add_package('multicol')
        super().__init__(self.name, content, env_modifiers=self._wrap_with_braces(str(self.num_cols)), **kwargs)
