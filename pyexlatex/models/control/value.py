from pyexlatex.models.item import SimpleItem


class Value(SimpleItem):
    name = 'value'

    def __init__(self, of: str, **kwargs):
        self.of = of

        super().__init__(self.name, self.of, **kwargs)
