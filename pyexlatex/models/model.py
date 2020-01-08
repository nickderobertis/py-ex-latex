from typing import Optional, Any, Dict, List
import os

from jinja2 import FileSystemLoader

from pyexlatex.models.jinja import JinjaTemplate, JinjaEnvironment, DataString
from pyexlatex.models.template import Template


class Model(Template):
    """
    A data model combined with a Jinja template.

    Passes any class variables and methods to template to render the output string.
    Subclass this class to create your own data models for templates.

    Set exclude_attrs class variable as a list of strings of any attributes which should not be
    passed to the template.

    Examples:

        >>> import pyexlatex as pl
        >>> template_str = "{{ my_var | Bold }} {{ my_link }} {{ my_text }}"
        >>>
        >>> class MyModel(pl.Model):
        >>>     my_var = 'woo'
        >>>     my_link = pl.Hyperlink('https://www.google.com', 'Link!!!!')
        >>>
        >>>     def __init__(self, my_text: str, *args, **kwargs):
        >>>         self.my_text = my_text
        >>>         super().__init__(*args, **kwargs)
        >>>
        >>> model = MyModel('stuff', template_str=template_str)
        >>> str(model)
        '\\textbf{woo} \\href{https://www.google.com}{Link!!!!} stuff '



    """
    # Additional attributes to exclude adding to template variables
    exclude_attrs: List[str] = []

    def __init__(self, template_str: Optional[str] = None, template_path: Optional[str] = None,
                 environment: Optional[JinjaEnvironment] = None):
        self.template_str = template_str
        self.template_path = template_path
        self._validate_template()
        self.environment = environment
        self.contents = self._get_contents()
        super().__init__()

    @property
    def environment(self):
        return self._environment

    @environment.setter
    def environment(self, env: Optional[JinjaEnvironment]):
        self._active_template_path = self.template_path
        if env is not None:
            self._environment = env
            return

        if self.template_path is not None:
            template_dir = os.path.dirname(os.path.realpath(self.template_path))
            template_name = os.path.basename(self.template_path)

            # Create environment with file system loader in the folder containing the template
            self._environment = JinjaEnvironment(loader=FileSystemLoader(template_dir))

            # Switch template path str passed to environment to just name, as environment was created in that folder
            self._active_template_path = template_name

        if self.template_str is not None:
            self._environment = JinjaEnvironment()


    @property
    def template(self) -> JinjaTemplate:
        if self.template_str is not None:
            return self.environment.from_string(self.template_str)

        # Get from path
        return self.environment.get_template(self._active_template_path)

    @property
    def render_dict(self) -> Dict[str, Any]:
        always_exclude_attrs = [
            'environment',
            'template',
            'template_str',
            'template_path',
            'render_dict',
            'contents',
            'format_contents',
            'add_data_from_content',
            'init_data',
            'data',
            'add_package',
            'equal_attrs',
            'exclude_attrs',
            'is_DocumentItem',
            'is_LatexItem',
            'join',
            'name',
            'next_level_down_class'
        ]
        full_exclude = always_exclude_attrs + self.exclude_attrs
        attrs = [item for item in dir(self) if item not in full_exclude and not item.startswith('_')]
        return {attr: getattr(self, attr) for attr in attrs}


    def _validate_template(self):
        if self.template_str is not None and self.template_path is not None:
            raise ValueError(f'only specify one of template_str, template_path. got {self.template_str} for '
                             f'template_str, {self.template_path} for template_path')
        if self.template_str is None and self.template_path is None:
            raise ValueError(f'must specify one of template_str, template_path. got {self.template_str} for '
                             f'template_str, {self.template_path} for template_path')

    def _get_contents(self) -> DataString:
        render_dict = self.render_dict
        self.add_data_from_content(render_dict)
        return self.template.render(**render_dict)
