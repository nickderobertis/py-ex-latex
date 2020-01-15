import re
from copy import deepcopy
from functools import partial
from typing import Sequence, List, Any, Callable

from jinja2 import Environment, Template

from pyexlatex.models.containeritem import ContainerItem
from pyexlatex.models.datastore import DataStore
from pyexlatex.models.documentsetup import DocumentSetupData
from pyexlatex.models.item import ItemBase
from pyexlatex.texgen.replacements.file import general_latex_replacements

UPPER_PATTERN = re.compile('[A-Z]')

current_template_data_store = None


def class_factory(latex_class, *args, **kwargs):
    item = latex_class(*args, **kwargs)
    global current_template_data_store
    current_template_data_store.add_data_from_content(item)
    return str(item)


def get_capitalized_items(items: Sequence[str]) -> List[str]:
    return [name for name in items if UPPER_PATTERN.match(name[0])]


class JinjaTemplate(Template, ContainerItem):
    """
    A jinja Template but with pyexlatex models as built-in filters and handling extracting pyexlatex data

    Examples:

        >>> import pyexlatex as pl
        >>> str(pl.JinjaTemplate('{{ my_var | Italics }}').render(my_var='woo'))
        '\\textit{woo}'
    """

    def __new__(cls, source, **kwargs):
        env = JinjaEnvironment(**kwargs)
        return env.from_string(source, template_class=cls)

    def __init__(self, *args, **kwargs):
        pass

    def render(self, *args, **kwargs):
        format_dict = dict(*args, **kwargs)
        self.add_data_from_content(format_dict)

        # Set as current global template for adding data during filters
        _set_data_store_to_object(self)

        string = super().render(*args, **kwargs)
        return DataString(string, self.data)

    def __deepcopy__(self, memo):
        # TODO [#15]: Simplify Jinja template integration
        #
        # may be able to remove the __deepcopy__ method once https://github.com/pallets/jinja/issues/758 is resolved

        # Boilerplate deepcopy
        cls = self.__class__

        # The one modification to boilerplate deepcopy, originally cls and not object
        # Create instance without using JinjaTemplate.__new__
        # This is the way it is being done in Template._from_namespace and it avoids an error during
        # deepcopy that source is not defined
        result = object.__new__(cls)

        # Continue boilerplate deepcopy
        memo[id(self)] = result
        for k, v in self.__dict__.items():
            setattr(result, k, deepcopy(v, memo))
        return result



class DataString(ItemBase):

    def __init__(self, string: str, data: DocumentSetupData):
        super().__init__()
        self.content = string
        self.data = data

    def __str__(self):
        return general_latex_replacements(self.content)


class JinjaEnvironment(Environment):
    """
    A jinja Environment but with pyexlatex models as built in filters and handling extracting pyexlatex data

    Examples:

        >>> import pyexlatex as pl
        >>> from jinja2 import DictLoader
        >>> env = pl.JinjaEnvironment(
        >>>     loader=DictLoader({'my_temp': '{{ my_var | Italics }}'})
        >>> )
        >>> temp = env.get_template('my_temp')
        >>> str(temp.render(my_var='woo'))
        '\\textit{woo}'

    """
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

    def from_string(self, *args, **kwargs):
        return _template_factory(
            super().from_string,
            *args,
            **kwargs
        )

    def _load_template(self, *args, **kwargs):
        return _template_factory(
            super()._load_template,
            *args,
            **kwargs
        )


def _set_data_store_to_temporary_object():
    """
    Capture data by using a temporary object
    :return:
    """
    temp_obj = DataStore()
    _set_data_store_to_object(temp_obj)
    return temp_obj


def _set_data_store_to_object(obj: Any):
    global current_template_data_store
    current_template_data_store = obj


def _template_factory(factory_func: Callable, *args, **kwargs) -> JinjaTemplate:
    """
    Handles creating jinja template complete with pyexlatex data.

    Manages a temporary global data store so that jinja filters can add to that data store, then after creating
    the template, the data is added to the template.

    :param factory_func: function which should return a Template
    :param args: passed to factory_func
    :param kwargs: passed to factory_func
    """
    # Set current global data store for adding data during filters
    data_store = _set_data_store_to_temporary_object()

    # Create object in usual jinja way
    actual_template = factory_func(*args, **kwargs)

    # Add data to newly created object
    actual_template.data = data_store.data

    return actual_template

