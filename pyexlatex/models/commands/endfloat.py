from pyexlatex.models.item import MultiOptionSimpleItem


class DeclareDelayedFloatFlavor(MultiOptionSimpleItem):
    name = 'DeclareDelayedFloatFlavor'
    equal_attrs = [
        'name',
        'target_environment',
        'treat_as_environment'
    ]

    def __init__(self, target_environment: str, treat_as_environment: str = 'table'):
        self.target_environment = target_environment
        self.treat_as_environment = treat_as_environment
        super().__init__(self.name, target_environment, treat_as_environment)
