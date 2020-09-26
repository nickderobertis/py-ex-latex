from typing import Type

from pyexlatex import Italics, EnvironmentTemplate
from pyexlatex.letter.letter import Letter
from pyexlatex.models.environment import Environment
from pyexlatex.models.landscape import Landscape


class TextAreaTest:
    area_class: Type = Italics
    tag_name: str = 'section'

    def test_str(self):
        content = self.area_class('woo')
        assert str(content) == '\\' + self.tag_name + '{woo}'

    def test_list(self):
        content = self.area_class(['woo', 'yeah'])
        assert str(content) == '\\' + self.tag_name + '{woo\nyeah}'


class EnvironmentTest:
    env_class: Type = Letter
    tag_name: str = 'environment'

    def test_no_modifiers(self):
        content = self.env_class().wrap('woo')
        braces_tag_name = f'{{{self.tag_name}}}'
        assert str(content) == f'\\begin{braces_tag_name}\nwoo\n\end{braces_tag_name}'

    def test_modifiers(self):
        modifier_str = '{stuff}'
        content = self.env_class(modifiers=modifier_str).wrap('woo')
        braces_tag_name = f'{{{self.tag_name}}}'
        assert str(content) == f'\\begin{braces_tag_name}{modifier_str}\nwoo\n\end{braces_tag_name}'