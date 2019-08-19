from pyexlatex.models.item import Item

class FileContents(Item):
    name = 'filecontents'

    def __init__(self, contents, filename: str):
        super().__init__(self.name, contents, env_modifiers=f'{{{filename}}}')