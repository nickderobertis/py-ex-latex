from pyexlatex.models.item import SimpleItem
from pyexlatex.models.package import Package


class Cite(SimpleItem):
    name = 'cite'

    def __init__(self, item_accessor: str):
        super().__init__(self.name, item_accessor)


class NatBibCiteBase(Cite):

    def __init__(self, item_accessor):
        self.init_data()
        self.data.packages.append(Package('natbib'))
        return super().__init__(item_accessor)


class CiteT(NatBibCiteBase):
    name = 'citet'


class CiteP(NatBibCiteBase):
    name = 'citep'
