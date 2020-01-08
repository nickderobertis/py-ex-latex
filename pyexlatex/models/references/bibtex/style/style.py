from typing import Optional
from pyexlatex.models.item import SimpleItem
from pyexlatex.models.package import Package
from pyexlatex.models.control.filecontents import FileContents


class BibliographyStyle(SimpleItem):
    name = 'bibliographystyle'

    def __init__(self, contents):
        super().__init__(self.name, contents)


class Style(BibliographyStyle):

    def __init__(self, style_name: str, style_definition: Optional[str] = None):
        self.style_name = style_name
        self.style_definition = style_definition
        
        self.init_data()
        if self.style_definition is not None:
            self.data.filepaths.append(self.style_filename)
            self.data.binaries.append(bytes(self.style_definition, 'utf8'))

        super().__init__(self.style_source_name)


    @property
    def style_filename(self) -> str:
        return self.style_name + '.bst'

    @property
    def style_source_name(self) -> str:
        return 'Sources/' + self.style_name