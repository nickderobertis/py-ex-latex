from typing import Optional, Sequence
from pyexlatex.models.item import ItemBase
from pyexlatex.models.references.bibtex.base import BibTexEntryBase
from pyexlatex.models.references.bibtex.style.manager import StyleManager
from pyexlatex.models.control.filecontents import FileContents
from pyexlatex.models.containeritem import ContainerItem
from pyexlatex.models.package import Package
from pyexlatex.texgen import _basic_item_str


class Bibliography(ContainerItem, ItemBase):
    """
    High-level class for working with bibliographies in LaTeX. Handles style as well as the references.
    Include an instance of this class where you want the bibliography printed.
    """

    def __init__(self, references: Optional[Sequence[BibTexEntryBase]] = None, style_name: str = 'plain'):
        self.references = references
        style_manager = StyleManager()
        self.style = style_manager.get_style_by_name(style_name)
        self.add_data_from_content(self.style)
        self._include_references_file(references)
        self.data.packages.append(Package('natbib'))

    def _include_references_file(self, references: Optional[Sequence[BibTexEntryBase]] = None):
        from pyexlatex.logic.builder import _build
        all_references = _build(references)
        references_inline_file = FileContents(all_references, 'refs.bib')
        self.data.end_document_items.append(references_inline_file)
        self.data.packages.append(Package('filecontents'))

    def __str__(self):
        from pyexlatex.logic.builder import _build
        bibliography_str = _basic_item_str('bibliography', 'refs')
        output = _build([
            self.style,
            bibliography_str
        ])
        return output

        
