from pyexlatex.models.item import Item
from pyexlatex.models.documentitem import DocumentItem
from pyexlatex.logic.format.contents import format_contents


class Abstract(DocumentItem, Item):
    name = 'abstract'

    def __init__(self, content):
        content = format_contents(content)
        super().__init__(self.name, content)
