from typing import Optional
from pyexlatex.models.item import ItemBase


class DocumentClassType(ItemBase):

    def __init__(self, name: str, definition: Optional[str] = None):
        self.name = name
        self.definition = definition

        self.init_data()
        if self.definition is not None:
            self.data.filepaths.append(self.class_filename)
            self.data.binaries.append(bytes(self.definition, 'utf8'))

        super().__init__(self.style_source_name)

    @property
    def class_filename(self) -> str:
        return self.name + '.cls'

    @property
    def style_source_name(self) -> str:
        return 'Sources/' + self.name

    def __str__(self):
        return self.name
