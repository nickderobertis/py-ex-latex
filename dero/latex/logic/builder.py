from dero.latex.texgen import _centering_str
from dero.latex.table.models.texgen.breaks import LineBreak

def build_figure_content(items, caption=None, label=None, centering=True, position_str=None):
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
    return LineBreak().join(elements)