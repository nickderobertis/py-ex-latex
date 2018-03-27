from dero.latex.models import Environment
from dero.latex.models.mixins import StringAdditionMixin
from dero.latex.texgen import _basic_item_str

class Item(StringAdditionMixin):

    def __init__(self, name, contents):
        self.env = Environment(name)
        self.contents = contents

    def __repr__(self):
        return f'<Item(name={self.env.name}, contents={self.contents})>'

    def __str__(self):
        return self.env.wrap(self.contents)

class SimpleItem(StringAdditionMixin):

    def __init__(self, name, contents):
        self.name = name
        self.contents = contents

    def __repr__(self):
        return f'<{self.name.title()}({self.contents})>'

    def __str__(self):
        return _basic_item_str(self.name, self.contents)