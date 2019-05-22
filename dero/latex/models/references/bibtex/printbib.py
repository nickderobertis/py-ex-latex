from dero.latex.models.item import NoOptionsNoContentsItem

class PrintBibliography(NoOptionsNoContentsItem):
    name = 'printbibliography'

    def __init__(self):
        super().__init__(self.name)

