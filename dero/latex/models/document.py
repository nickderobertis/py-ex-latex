from dero.latex.models.environment import Environment
from dero.latex.models.item import Item
from dero.latex.texgen import _document_class_str

from dero.latex.models.landscape import Landscape

class DocumentEnvironment(Environment):
    name = 'document'

    def __init__(self):
        super().__init__(name=self.name)

class Document(Item):
    name = 'document'

    def __init__(self, packages, content, landscape=False):
        from dero.latex.logic.builder import _build
        self.packages = packages

        pre_env_contents = _build([
            _document_class_str(),
            *[str(package) for package in self.packages]
        ])

        if landscape:
            content = Landscape().wrap(str(content))

        super().__init__(self.name, content, pre_env_contents=pre_env_contents)

    def __repr__(self):
        return f'<Document>'