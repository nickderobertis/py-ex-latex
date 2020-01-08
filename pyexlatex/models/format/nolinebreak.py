from pyexlatex.models.template import Template
from pyexlatex.models.format.paragraph.raggedright import RaggedRight
from pyexlatex.models.format.paragraph.sloppy import Sloppy
from pyexlatex.models.format.text.nohyphens import NoHyphens


class NoLineBreak(Template):
    """
    Prevents a line break within text, where a hyphen would normally be placed.

    Notes:
        Using this will have side effects to the entire paragraph, depending on the alternative chosen. See
        the docstring for alternative.
    """
    name = 'nohyphens'

    def __init__(self, contents, alternative: str = 'ragged'):
        """

        :param contents:
        :param alternative: 'ragged' or 'sloppy'. As the word won't be broken, there must be some alternative.
            Passing 'ragged' will make all the other words on the first line stay in the same position, so that
            a gap will appear at the end of the line where the NoLineBreak word would have started originally. Passing
            'sloppy' will make it so that the first line's words spacing gets stretched so that there is still right
            alignment on that line, despite the NoLineBreak word being moved to the next line. Note: This will affect
            the entire paragraph, not just the NoLineBreak word.
        """
        self.alternative = alternative.lower()
        self.orig_contents = contents
        self._validate()

        self.contents = self._get_contents()

        super().__init__()

    def _get_contents(self):
        return [
            self._alternative_obj,
            NoHyphens(self.orig_contents)
        ]

    @property
    def _alternative_obj(self):
        if self.alternative == 'ragged':
            return RaggedRight()
        elif self.alternative == 'sloppy':
            return Sloppy()

    def _validate(self):
        self._validate_alternative()

    def _validate_alternative(self):
        alternatives = (
            'ragged',
            'sloppy',
        )
        if self.alternative not in alternatives:
            raise ValueError(f'Must pass valid alternative, one of {alternatives} to NoLineBreak. Got {self.alternative}')

