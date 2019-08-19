from pyexlatex.models.item import SimpleItem

class AddBibResource(SimpleItem):
    name = 'addbibresource'

    def __init__(self, bib_path: str):
        super().__init__(self.name, bib_path)
