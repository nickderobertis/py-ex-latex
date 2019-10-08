from typing import Union, Optional, TYPE_CHECKING
if TYPE_CHECKING:
    from pyexlatex.table import ColumnsAlignment


class BaseTabular:

    @staticmethod
    def _get_num_columns_from_content(content) -> int:
        # Content should be made a list before this function. Get first or only content back
        reference_content = content[0]

        # Try to get from num_columns attribute if it exists
        num_columns = getattr(reference_content, 'num_columns', None)
        if num_columns is not None:
            return num_columns

        # Otherwise, try to take the length of the first passed content
        return len(reference_content)

    def _get_columns_alignment_from_passed_align(self, content,
                                                 align: Optional[Union['ColumnsAlignment', str]] = None
                                                 ) -> 'ColumnsAlignment':
        from pyexlatex.table import ColumnsAlignment
        if align is None:
            return ColumnsAlignment(
                num_columns=BaseTabular._get_num_columns_from_content(content)
            )
        elif isinstance(align, str):
            return ColumnsAlignment.from_alignment_str(align)
        else:
            # Assumed to be passed ColumnsAlignment or something else that will directly work in its place
            return align