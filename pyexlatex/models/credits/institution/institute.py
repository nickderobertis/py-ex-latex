from typing import Optional, Sequence, List, Union, Dict
from pyexlatex.models.item import SimpleItem, ItemBase
from pyexlatex.models.credits.institution.inst import Inst
from pyexlatex.models.format.breaks import TableLineBreak
from pyexlatex.models.control.and_ import And


class Institutes(SimpleItem):
    """
    e.g. output
    \institute[VFU] % (optional)
    {
        \inst{1}%
        Faculty of Physics\\
        Very Famous University
        \and
        \inst{2}%
        Faculty of Chemistry\\
        Very Famous University
    }

    """
    name = 'institute'

    def __init__(self, institutions: Sequence[Sequence[str]], short_institution: Optional[str] = None):
        self.institutions = institutions
        self.short_institution = short_institution

        super().__init__(self.name, self.content_objs, pre_modifiers=self._wrap_with_bracket(short_institution))

    @property
    def content_objs(self) -> List[Union['Institution', And]]:
        # Eliminate duplicates in institutions, displaying unique ordered institutions
        count = 0
        counted_institutions: Dict[Sequence[str], int] = {}
        for inst_lines in self.institutions:
            inst_lines = tuple(inst_lines)
            if inst_lines not in counted_institutions:
                count += 1
                counted_institutions[inst_lines] = count

        content_objs = []
        for inst_lines, count in counted_institutions.items():
            content_objs.append(Institution(inst_lines, count))
            content_objs.append(And())
        content_objs = content_objs[:-1]  # strip last \and
        return content_objs


class Institution(ItemBase):
    """
    e.g.
        \inst{1}%
        Faculty of Physics\\
        Very Famous University
    """
    equal_attrs = [
        'institution_lines',
        'num'
    ]

    def __init__(self, institution_lines: Sequence[str], num: int):
        self.institution_lines = institution_lines
        self.num = num

    def __str__(self) -> str:
        from pyexlatex.logic.builder import _build
        inst = Inst(self.num)
        inst_output = TableLineBreak().join(self.institution_lines)
        return _build([
            inst,
            inst_output
        ])
