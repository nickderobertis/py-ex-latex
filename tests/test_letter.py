from pyexlatex import LetterDocument
from pyexlatex.letter.closing import Closing
from pyexlatex.letter.enclosures import Enclosures
from pyexlatex.letter.letter import Letter
from pyexlatex.letter.opening import Opening
from pyexlatex.letter.ps import PS
from pyexlatex.letter.signature import Signature
import pyexlatex as pl
from tests.base import TextAreaTest, EnvironmentTest


class TestClosing(TextAreaTest):
    area_class = Closing
    tag_name = 'closing'


class TestEnclosures(TextAreaTest):
    area_class = Enclosures
    tag_name = 'encl'


class TestOpening(TextAreaTest):
    area_class = Opening
    tag_name = 'opening'


class TestPS(TextAreaTest):
    area_class = PS
    tag_name = 'ps'


class TestSignature(TextAreaTest):
    area_class = Signature
    tag_name = 'signature'


class TestLetter(EnvironmentTest):
    env_class = Letter
    tag_name = 'letter'


class TestLetterDocument:
    no_options_result = '\\documentclass[]{letter}\n\\longindentation=0pt\n\\begin{document}\n\\begin{letter}{}\n\\opening{Dear Sir or Madam:}\nwoo\n\\closing{Sincerely,}\n\\end{letter}\n\\end{document}'

    def test_no_options_str(self):
        doc = LetterDocument('woo')
        assert str(doc) == self.no_options_result

    def test_no_options_list(self):
        doc = LetterDocument(['woo'])
        assert str(doc) == self.no_options_result

    def test_auto_package_inclusion(self):
        doc = LetterDocument(['woo', pl.RGB(10, 20, 30, color_name='cool')])
        assert str(doc) == '\\documentclass[]{letter}\n\\usepackage{xcolor}\n\\longindentation=0pt\n\\begin{document}\n\\begin{letter}{}\n\\opening{Dear Sir or Madam:}\nwoo\n\\definecolor{cool}{RGB}{10,20,30}\n\\closing{Sincerely,}\n\\end{letter}\n\\end{document}'

    def test_all_options(self):
        doc = LetterDocument(
            'woo',
            contact_info=['my name','123 main st', 'my city, state'],
            to_contact_info=['your name', '456 main st', 'their city, state'],
            signer_name='my name twice',
            closing_indent='5pt',
            salutation='yo girl:',
            closing='yours forever and ever',
            ps='an extra thought!',
            enclosures=['one thing', 'another thing'],
        )
        assert str(doc) == '\\documentclass[]{letter}\n\\address{my name \\\\ 123 main st \\\\ my city, state}\n\\signature{my name twice}\n\\longindentation=5pt\n\\begin{document}\n\\begin{letter}{your name \\\\ 456 main st \\\\ their city, state}\n\\opening{yo girl:}\nwoo\n\\closing{yours forever and ever}\n\\ps{an extra thought!}\n\\encl{one thing\nanother thing}\n\\end{letter}\n\\end{document}'
