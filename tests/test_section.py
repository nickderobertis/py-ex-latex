from typing import Type

from pyexlatex.models.section.sections import SubSubSection, SubSection, Section, Chapter


class TextSectionTest:
    item_class: Type = Section
    tag_name: str = 'section'

    def test_str(self):
        content = self.item_class('woo', title='title')
        braces_tag_name = f'{{{self.tag_name}}}'
        assert str(content) == f'\\begin{braces_tag_name}{{title}}\nwoo\n\end{braces_tag_name}'


class TestSubSubSection(TextSectionTest):
    item_class = SubSubSection
    tag_name = 'subsubsection'


class TestSubSection(TextSectionTest):
    item_class = SubSection
    tag_name = 'subsection'


class TestSection(TextSectionTest):
    item_class = Section
    tag_name = 'section'


class TestChapter(TextSectionTest):
    item_class = Chapter
    tag_name = 'chapter'


def test_sections_from_dict():
    contents = {
        'S One': 'Content for S One',
        'S Two': {
            'SS One': 'Content for SS One',
            'SS Two': {
                'SSS One': 'Content for SSS One',
            }
        },
    }
    content = Chapter(contents, title='C One')
    assert str(content) == '\\begin{chapter}{C One}\n\\begin{section}{S One}\nContent for S One\n\\end{section}\n\\begin{section}{S Two}\n\\begin{subsection}{SS One}\nContent for SS One\n\\end{subsection}\n\\begin{subsection}{SS Two}\n\\begin{subsubsection}{SSS One}\nContent for SSS One\n\\end{subsubsection}\n\\end{subsection}\n\\end{section}\n\\end{chapter}'
