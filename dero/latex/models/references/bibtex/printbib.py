from dero.latex.models.item import NoOptionsNoContentsItem
from dero.latex.models.documentitem import DocumentItem

class PrintBibliography(NoOptionsNoContentsItem, DocumentItem):
    name = 'printbibliography'

    def __init__(self):
        super().__init__(self.name)

