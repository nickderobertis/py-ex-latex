from dero.latex.models.item import Item
from dero.latex.models.documentitem import DocumentItem
from dero.latex.logic.format.contents import format_contents


class Abstract(DocumentItem, Item):
    name = 'abstract'

    def __init__(self, content):
        content = format_contents(content)
        super().__init__(self.name, content)
