from typing import Optional, Sequence, Union
from dero.latex.models.item import SimpleItem
from dero.latex.models.credits.institution.inst import Inst
from dero.latex.models.credits.institution.institute import Institutes


class Author(SimpleItem):
    name = 'author'

    def __init__(self, authors: Union[str, Sequence[str]], short_author: Optional[str] = None,
                 institutions: Optional[Sequence[Sequence[str]]] = None, short_institution: Optional[str] = None):
        if isinstance(authors, str):
            authors = [authors]
        self.authors = authors
        self.short_author = short_author if short_author is not None else authors[0]
        self.institutions = institutions
        self.short_institution = short_institution
        self._validate()
        self.institution_nums = []
        self._setup_institutions()

        super().__init__(self.name, self.content, pre_modifiers=self._wrap_with_bracket(self.short_author))

    @property
    def content(self):
        if self.institutions is None:
            return self.authors

        content = []
        for i, author in enumerate(self.authors):
            content.append(author + Inst(self.institution_nums[i]))
        return ', '.join(content)

    def _validate(self):
        if self.institutions is not None:
            self._check_lengths_match_raise_value_error_if_not(
                self.authors,
                self.institutions,
                'authors',
                'instutitions'
            )

    def _setup_institutions(self):
        if self.institutions is None:
            return
        # Number institutions starting with 1, but if institution already has a number then use that again
        count = 0
        counted_institutions = {}
        for institution in self.institutions:
            institution = tuple(institution)
            if institution not in counted_institutions:
                count += 1
                counted_institutions[institution] = count
            self.institution_nums.append(counted_institutions[institution])

        self._check_lengths_match_raise_value_error_if_not(
            self.institutions,
            self.institution_nums,
            'instutitions',
            'institution_nums'
        )

        self.init_data()
        institutes_def = Institutes(self.institutions, short_institution=self.short_institution)
        self.data.packages.append(institutes_def)

    def _check_lengths_match_raise_value_error_if_not(self, item1: Sequence, item2: Sequence,
                                                      item1_name: str, item2_name: str):
        len_item_1 = len(item1)
        len_item_2 = len(item2)
        if len_item_1 != len_item_2:
            raise ValueError(f'number of {item1_name} must match that of {item2_name}. got {len_item_1} '
                             f'{item1_name} and {len_item_2} {item2_name}')