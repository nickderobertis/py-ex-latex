from typing import Optional, Sequence, Union, List
from pyexlatex.models.item import SimpleItem
from pyexlatex.models.credits.institution.inst import Inst
from pyexlatex.models.credits.institution.institute import Institutes


class Author(SimpleItem):
    name = 'author'
    institution_nums: List[int]

    def __init__(self, authors: Union[str, Sequence[str]], short_author: Optional[str] = 'auto',
                 institutions: Optional[Sequence[Sequence[str]]] = None, short_institution: Optional[str] = None):
        """

        :param authors:
        :param short_author: pass short name for author, 'auto' to automatically use first author as short author,
            or None for there to be no short name
        :param institutions:
        :param short_institution:
        """
        if isinstance(authors, str):
            authors = [authors]
        self.authors = authors
        self.short_author = short_author
        self.institutions = institutions
        self.short_institution = short_institution
        self._validate()
        self.institution_nums = []
        self._setup_institutions()
        self.content = self._get_content()

        super().__init__(self.name, self.content, pre_modifiers=self._short_author_modifiers_str)

    @property
    def _short_author_modifiers_str(self) -> Optional[str]:
        if self.short_author is None:
            return None

        if self.short_author.lower() == 'auto':
            short_author = self.authors[0]
        else:
            short_author = self.short_author

        return self._wrap_with_bracket(short_author)


    def _get_content(self):
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