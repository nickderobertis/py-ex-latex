from dero.latex.texgen import _centering_str

def build_content(items, caption=None, label=None, centering=True, position_str=None):
    elements = [
        position_str,
        _centering_str() if centering else None,
        *[str(item) for item in items],
        str(caption) if caption else None,
        str(label) if label else None
    ]

    valid_elements = [elem for elem in elements if elem]

    return _build(valid_elements)

def _build(elements):
    return '\n'.join(elements)