import os
import runpy
import tempfile
from copy import deepcopy
from pathlib import Path
from typing import List, Dict, Any

from docutils.nodes import Node
from docutils.statemachine import StringList
from sphinx.util.docutils import SphinxDirective
from docutils import nodes

from pyexlatex.models.document import DocumentBase

PDFS_PATH = Path(__file__).parent.parent / "source" / "_static" / "pdfs"


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


def _create_internal_pyexlatex_script(content: StringList) -> str:
    # Name last variable as output
    out_content = list(content)
    out_content[-1] = f"output = {out_content[-1]}"

    # Add import
    out_content.insert(0, "import pyexlatex as pl")
    return "\n".join(out_content)


def _create_displayed_pyexlatex_script(content: StringList) -> str:
    return "\n".join(content)


def _run_source_extract_globals(source: str) -> Dict[str, Any]:
    f = tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False)
    f.write(source)
    f.close()
    globs = runpy.run_path(f.name)
    os.remove(f.name)
    return globs


def _run_pyexlatex_build_from_source(source: str, name: str):
    globs = _run_source_extract_globals(source)
    output: DocumentBase = globs["output"]
    output.to_pdf(PDFS_PATH, name)


def _pdf_src(name: str) -> str:
    return f"_static/pdfs/{name}.pdf"


class PyexlatexExample(SphinxDirective):
    required_arguments = 1
    has_content = True

    def run(self) -> List[Node]:
        name: str = self.arguments[0]
        pyexlatex_internal_script = _create_internal_pyexlatex_script(self.content)
        _run_pyexlatex_build_from_source(pyexlatex_internal_script, name)
        displayed_script_content = _create_displayed_pyexlatex_script(self.content)
        return [
            nodes.literal_block(text=displayed_script_content),
            pdf_iframe(_pdf_src(name)),
        ]
