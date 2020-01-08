
def _remove_backslashes(latex_str):
    return ''.join([letter for letter in latex_str if letter != '\\'])