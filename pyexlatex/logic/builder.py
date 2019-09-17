from pyexlatex.models.format.breaks import LineBreak

def build_figure_content(items, caption=None, label=None, centering=True, position_str=None):
    from pyexlatex.texgen import _centering_str
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


def build(content):
    if hasattr(content, 'contents'):
        result = build(content.contents)
        content.contents = result
    if hasattr(content, 'content'):
        result = build(content.content)
        content.content = result
    if hasattr(content, 'contents') or hasattr(content, 'content'):
        return content
    elif isinstance(content, (list, tuple)):
        built = _build([build(c) for c in content])
        return built
    elif content is None:
        return ''
    else:
        return str(content)
