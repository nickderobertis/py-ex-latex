from pyexlatex.models.item import SimpleItem

class ExtraFloats(SimpleItem):
    name = 'extrafloats'

    def __init__(self, num_extra: int = 1000):
        super().__init__(self.name, str(num_extra))
