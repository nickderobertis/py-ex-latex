from pyexlatex.models.item import SimpleItem


class NewCounter(SimpleItem):
    name = 'newcounter'

    def __init__(self, counter_name: str, **kwargs):
        self.counter_name = counter_name

        super().__init__(self.name, self.counter_name, **kwargs)
