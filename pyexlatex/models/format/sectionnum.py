from typing import Dict, List
from pyexlatex.models.commands.renewcommand import ReNewCommand


class SectionNumberingFormatter(ReNewCommand):
    """
    applies formatting for section numbers
    """

    def __init__(self, section_type: str, section_format: str):
        section_type_format_command_name = f'the{section_type}'  # e.g. \thesection \thesubsection
        super().__init__(section_type_format_command_name, section_format)

    @classmethod
    def list_from_string_format_dict(cls, string_format_dict: Dict[str, str]) -> List['SectionNumberingFormatter']:
        """

        Args:
            string_format_dict: e.g. dict(
                section=r'\Roman{section}',
                subsection=r'\Alph{subsection}'
            )

        Returns:

        """
        formatters = []
        for section_type, section_format in string_format_dict.items():
            formatters.append(
                cls(section_type, section_format)
            )
        return formatters

