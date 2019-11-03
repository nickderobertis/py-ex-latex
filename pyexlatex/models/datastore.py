from pyexlatex.models.containeritem import ContainerItem
from pyexlatex.models.documentitem import DocumentItem


class DataStore(ContainerItem, DocumentItem):
    """
    Holds LaTeX item data and can be included directly in documents. Mainly for internal use.
    """

    def __init__(self, content=None):
        if content is not None:
            self.add_data_from_content(content)
        else:
            self.init_data()

    def __str__(self):
        return ''
