from dero.latex.models.item import SimpleItem


class Cite(SimpleItem):
    name = 'cite'

    def __init__(self, item_accessor: str):
        super().__init__(self.name, item_accessor)


class CiteT(Cite):
    name = 'citet'


class CiteP(Cite):
    name = 'citep'
