from pyexlatex.models.item import MultiOptionSimpleItem
from mixins.attrequals import EqOnAttrsWithConversionMixin, EqHashMixin


class NewEnvironment(MultiOptionSimpleItem, EqOnAttrsWithConversionMixin, EqHashMixin):
    name = 'newenvironment'
    equal_attrs = ['env_name', 'begin', 'end']
    convert_type = str

    def __init__(self, env_name: str, begin_env: str, end_env: str):
        self.env_name = env_name
        self.begin = begin_env
        self.end = end_env
        super().__init__(self.name, env_name, begin_env, end_env)

