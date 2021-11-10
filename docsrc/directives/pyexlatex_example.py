from typing import List

from docutils.nodes import Node
from sphinx.util.docutils import SphinxDirective
from docutils import nodes


def html(content: str) -> nodes.raw:
    return nodes.raw(text=content, format="html")


def pdf_iframe(src: str) -> nodes.raw:
    content = f"""
<iframe 
    id="ID" 
    style="border:1px solid #666CCC" 
    title="PDF" 
    src="{src}" 
    frameborder="1" 
    scrolling="auto" 
    height="600" 
    width="100%" 
    align="middle"
></iframe>
    """
    return html(content)


class PyexlatexExample(SphinxDirective):
    has_content = True

    def run(self) -> List[Node]:
        full_content = "\n".join(self.content)
        # breakpoint()
        return [
            nodes.literal_block(text=full_content),
            pdf_iframe("_static/pdfs/basic_presentation.pdf"),
        ]
