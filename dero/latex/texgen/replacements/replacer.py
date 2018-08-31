from typing import Dict, List

latex_escape_character = '\\' # literal \
latex_replacement_items = ['%', '&', '_']
replacement_dict = {
        latex_replacement_item: latex_escape_character + latex_replacement_item \
        for latex_replacement_item in latex_replacement_items
    }

class Replacer:

    def __init__(self, replacement_dict: Dict[str, str], escape_character: str=None):
        self.replacement_dict = replacement_dict
        self.escape_character = escape_character

    def replace(self, string: str) -> str:
        possible_replacement = ''
        replacing = False
        output_str = ''
        previous_letter = ''
        for letter in string:
            wipe_replacement = True # wipe unless told not to by the loop
            ### TEMP
            # import pdb
            # pdb.set_trace()
            ### END TEMP
            output_letter = letter
            possible_replacement += letter

            # automatically is skipped if longer than one letter, so won't enter while replacing
            if possible_replacement in self.first_letters:
                if previous_letter == self.escape_character:
                    # Escape character. No need to replace. Start over
                    replacing = False
                else:
                    # may be something to replace
                    replacing = True
                    # Handle single character replacements
                    if possible_replacement in self.unique_full_first_letter_replacements:
                        # Got a replacement.
                        # Do replacement
                        output_letter = self.unique_full_first_letter_replacements[possible_replacement]
                        # Reset for next replacement
                        replacing = False

            if replacing:
                # Handle multiple character replacements
                current_replacements = _replacements_starting_with(
                    possible_replacement, self.replacement_dict
                )
                if current_replacements == {}:
                    # No replacements found. Start over
                    replacing = False
                else:
                    # Matching replacements. Determine whether may be another replacement key prefixed by this one
                    if len(current_replacements) == 1:
                        # Single replacement. If it's a full replacement, do it
                        if list(current_replacements.keys())[0] in self.replacement_dict:
                            output_letter = current_replacements[possible_replacement]
                            # Reset for next replacement
                            replacing = False

                        else:
                            # we haven't gotten to the end of this replacement yet, continue until end
                            wipe_replacement = False
                    else:
                        # Multiple matching replacements, continue until only one match
                        wipe_replacement = False

            if wipe_replacement:
                possible_replacement = ''

            previous_letter = letter # Maybe should set to output letter? doesn't matter for current use cases
            output_str += output_letter

        return output_str

    @property
    def first_letters(self) -> List[str]:
        if hasattr(self, '_first_letters'):
            return self._first_letters

        self._first_letters = self._extract_first_letters()
        return self._first_letters

    def _extract_first_letters(self) -> List[str]:
        return _extract_letters_of_index_n(0, self.replacement_dict)

    @property
    def unique_full_first_letter_replacements(self) -> Dict[str, str]:
        if hasattr(self, '_unique_full_first_letter_replacements'):
            return self._unique_full_first_letter_replacements

        self._unique_full_first_letter_replacements = self._extract_unique_full_first_letter_replacements()
        return self._unique_full_first_letter_replacements

    def _extract_unique_full_first_letter_replacements(self) -> Dict[str, str]:
        first_letters_set = set(self.first_letters)
        unique_letters = [letter for letter in first_letters_set if self.first_letters.count(letter) == 1]

        replacements = {}
        for letter in unique_letters:
            replacements.update(_full_replacements_starting_with(letter, self.replacement_dict))

        return replacements


def _full_replacements_starting_with(starts_with_str: str, replacement_dict) -> Dict[str, str]:
    replacements = _replacements_starting_with(starts_with_str, replacement_dict)
    return {key: value for key, value in replacements.items() if len(key) == len(starts_with_str)}

def _replacements_starting_with(starts_with_str: str, replacement_dict) -> Dict[str, str]:
    replacements = replacement_dict.copy()
    for n, letter in enumerate(starts_with_str):
        replacements = _extract_replacements_where_letter_matches_index_n(n, letter, replacements)

    return replacements


def _extract_letters_of_index_n(n: int, dict_: dict) -> List[str]:
    return [key[n] for key in dict_]

def _extract_replacements_where_letter_matches_index_n(n: int, letter: str, dict_: dict) -> Dict[str, str]:
    return {key: value for key, value in dict_.items() if key[n] == letter}


latex_replacer = Replacer(replacement_dict, escape_character=latex_escape_character)