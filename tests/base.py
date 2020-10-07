import os
from typing import Type
import pathlib

from pyexlatex import Italics, EnvironmentTemplate, Footnote
from pyexlatex.letter.letter import Letter
from pyexlatex.models.environment import Environment
from pyexlatex.models.format.centering import Centering
from pyexlatex.models.item import MultiOptionSimpleItem
from pyexlatex.models.landscape import Landscape

TESTS_DIR = pathlib.Path(__file__).parent
INPUT_FILES_DIR = TESTS_DIR / 'input_files'
EXAMPLE_IMAGE_PATH = INPUT_FILES_DIR / 'nd-logo.png'
GENERATED_FILES_DIR = TESTS_DIR / 'generated_files'

if not os.path.exists(GENERATED_FILES_DIR):
    os.makedirs(GENERATED_FILES_DIR)


class NoOptionsNoContentsItemTest:
    item_class: Type = Centering
    tag_name: str = 'centering'

    def test_item(self):
        content = self.item_class()
        assert str(content) == '\\' + self.tag_name


class SimpleItemTest:
    item_class: Type = Footnote
    tag_name: str = 'footnote'

    def test_item(self):
        content = self.item_class('woo')
        assert str(content) == '\\' + self.tag_name + '{woo}'


class MultiOptionSimpleItemTest:
    item_class: Type = MultiOptionSimpleItem
    tag_name: str = 'footnote'

    def test_one_item(self):
        content = self.item_class('woo')
        assert str(content) == '\\' + self.tag_name + '{woo}'

    def test_two_items(self):
        content = self.item_class('woo', 'yeah')
        assert str(content) == '\\' + self.tag_name + '{woo}'


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