import re
from functools import partial
from typing import Sequence, List

from jinja2 import Environment, Template

from pyexlatex.models.containeritem import ContainerItem
from pyexlatex.models.documentsetup import DocumentSetupData
from pyexlatex.models.item import ItemBase

UPPER_PATTERN = re.compile('[A-Z]')


def class_factory(latex_class, *args, **kwargs):
    return str(latex_class(*args, **kwargs))


def get_capitalized_items(items: Sequence[str]) -> List[str]:
    return [name for name in items if UPPER_PATTERN.match(name[0])]


class JinjaTemplate(Template, ContainerItem):

    def __new__(cls, source, **kwargs):
        env = JinjaEnvironment(**kwargs)
        return env.from_string(source, template_class=cls)

    def __init__(self, *args, **kwargs):
        pass

    def render(self, *args, **kwargs):
        format_dict = dict(*args, **kwargs)
        self.add_data_from_content(format_dict)
        string = super().render(*args, **kwargs)
        return DataString(string, self.data)


class DataString(ItemBase):

    def __init__(self, string: str, data: DocumentSetupData):
        super().__init__()
        self.content = string
        self.data = data

    def __str__(self):
        return self.content


class JinjaEnvironment(Environment):
    template_class = JinjaTemplate

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._add_filters()

    def _add_filters(self):
        import pyexlatex as pl
        import pyexlatex.table as lt
        import pyexlatex.presentation as lp
        import pyexlatex.graphics as lg
        import pyexlatex.layouts as ll
        import pyexlatex.figure as lf

        for module in [pl, lt, lp, lg, ll, lf]:
            latex_class_names = get_capitalized_items(dir(module))
            for latex_class_name in latex_class_names:
                latex_class = getattr(module, latex_class_name)
                this_class_factory = partial(class_factory, latex_class)
                self.filters[latex_class_name] = this_class_factory