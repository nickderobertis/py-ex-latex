from pyexlatex.models.mixins import StringAdditionMixin
from pyexlatex.models.format.breaks import LineBreak

# TODO [#20]: Make new column types more flexible.
#
# Currently just passes full strings

class NewColumnTypes(StringAdditionMixin):

    def __init__(self):
        self.contents: [NewColumnType] = [
            NewColumnType(r'\newcolumntype{L}[1]{>{\raggedright\let\newline\\\arraybackslash\hspace{0pt}}m{#1}}'),
            NewColumnType(r'\newcolumntype{C}[1]{>{\centering\let\newline\\\arraybackslash\hspace{0pt}}m{#1}}'),
            NewColumnType(r'\newcolumntype{R}[1]{>{\raggedleft\let\newline\\\arraybackslash\hspace{0pt}}m{#1}}'),
            NewColumnType(r'\newcolumntype{.}{D{.}{.}{-1}}')
        ]

    def __str__(self):
        return LineBreak().join(self.contents)



class NewColumnType(str):
    pass