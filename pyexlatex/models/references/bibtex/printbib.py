from pyexlatex.models.item import NoOptionsNoContentsItem
from pyexlatex.models.documentitem import DocumentItem

class PrintBibliography(NoOptionsNoContentsItem, DocumentItem):
    name = 'printbibliography'

    def __init__(self):
        super().__init__(self.name)

