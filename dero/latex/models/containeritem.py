from dero.latex.models.documentitem import DocumentItem
from dero.latex.logic.extract.get import get_attr_from_items_or_collection
from dero.latex.models.documentsetup import DocumentSetupData


class ContainerItem(DocumentItem):
    """
    Inherit to be able to include LaTeX objects inside LaTeX objects
    """

    def __init__(self, name, content, *args, **kwargs):
        self.add_data_from_content(content)
        return super().__init__(name, content, *args, **kwargs)

    def add_data_from_content(self, content):
        self.init_data()
        aggregate_attributes = self.data.attrs
        for attr in aggregate_attributes:
            data_attr = getattr(self.data, attr)
            new_values = get_attr_from_items_or_collection(content, attr, unique=True)
            data_attr.extend(new_values)

    def init_data(self):
        if not hasattr(self, 'data'):
            self.data = DocumentSetupData()

