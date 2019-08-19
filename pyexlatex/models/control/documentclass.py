from typing import Optional
from pyexlatex.models.item import SimpleItem

class DocumentClass(SimpleItem):
    name = 'documentclass'

    def __init__(self, document_type: str = 'article', font_size: Optional[float] = 11,
                 num_columns: Optional[int] = None):
        self.document_type = document_type
        self.font_size = font_size
        self.num_columns = num_columns
        super().__init__(self.name, document_type, pre_modifiers=self._pre_modifiers_str)

    @property
    def _pre_modifiers_str(self) -> str:
        options = []
        if self.font_size is not None:
            options.append(f'{self.font_size}pt')
        if self.num_columns is not None:
            options.append(self._num_columns_str)

        options_str = ', '.join(options)
        return f'[{options_str}]'

    def _validate(self):
        if self.font_size is not None:
            if self.font_size not in (10, 11, 12):
                raise NotImplementedError(f'need to add a package to use font size other than 10, 11, 12, '
                                          f'got {self.font_size}')
        if self.num_columns is not None:
            if self.num_columns not in (1, 2):
                raise NotImplementedError(f'need to use the multicol package to get other than 1, 2 columns, '
                                          f'got {self.num_columns}')

    @property
    def _num_columns_str(self) -> str:
        if self.num_columns == 1:
            return 'onecolumn'
        if self.num_columns == 2:
            return 'twocolumn'
        return ''
