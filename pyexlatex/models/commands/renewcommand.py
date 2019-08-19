from pyexlatex.models.item import MultiOptionSimpleItem


class ReNewCommand(MultiOptionSimpleItem):
    name = 'renewcommand'

    def __init__(self, command_name: str, command_definition: str):
        super().__init__(self.name, rf'\{command_name}', command_definition)
