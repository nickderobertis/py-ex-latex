from dero.latex.models.environment import Environment
from dero.latex.models.item import Item
from dero.latex.texgen import _document_class_str
from dero.latex.models.package import Package
from dero.latex.logic.builder import _build

class DocumentEnvironment(Environment):
    name = 'document'

    def __init__(self):
        super().__init__(name=self.name)

class Document(Item):
    name = 'document'

    def __init__(self, package_str_list, content):
        self.packages = [Package(package_str) for package_str in package_str_list]

        contents = _build([
            _document_class_str(),
            *[str(package) for package in self.packages],
            str(content)
        ])

        super().__init__(self.name, contents)

    def __repr__(self):
        return f'<Document>'