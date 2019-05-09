from typing import List


class LatexError:

    def __init__(self, filename: str, line: int, context: List[str]):
        self.filename = filename
        self.line = line
        self.context = context

    @property
    def error(self):
        strip_chars = len(f'{self.filename}:{self.line}: ')
        return self.text[strip_chars:]

    @property
    def text(self):
        return ''.join(self.context)

    def __repr__(self):
        return f'<LatexError({self.error})>'
