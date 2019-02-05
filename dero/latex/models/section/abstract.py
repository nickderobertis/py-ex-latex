from dero.latex.models.item import Item
from dero.latex.models.documentitem import DocumentItem


class Abstract(DocumentItem, Item):
    name = 'abstract'

    def __init__(self, content):
        super().__init__(self.name, content)
