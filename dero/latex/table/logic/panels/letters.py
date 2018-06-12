from string import ascii_uppercase

def panel_string(i: int):
    return f'Panel {_panel_character(i)}: '

def _panel_character(i: int):
    if i < 0:
        raise ValueError('must pass positive index for panel character')
    if i > 26:
        raise NotImplementedError('need to work on panel letters greater than Z')

    return ascii_uppercase[i]
