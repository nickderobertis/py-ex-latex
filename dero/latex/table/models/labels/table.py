from dero.latex.table.models.table.section import TableSection
from dero.latex.table.models.labels.collection import LabelCollection


class LabelTable(TableSection):

    def __init__(self, label_collections: [LabelCollection]):
        self.label_collections = label_collections
        super().__init__()