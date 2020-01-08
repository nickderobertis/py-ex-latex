from pyexlatex.models.item import SimpleItem


class Monospace(SimpleItem):
    """
    Pass text to render it in a monospace font.
    """
    name = 'texttt'

    def __init__(self, content, **kwargs):
        super().__init__(self.name, content, **kwargs)