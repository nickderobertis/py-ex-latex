from typing import List
import bibtexparser
from bibtexparser.bibdatabase import BibDatabase
from pyexlatex.models.references.bibtex.generic import BibTexEntry


def extract_bibtex_str(bibtex: str) -> List[BibTexEntry]:
    bib_db: BibDatabase = bibtexparser.loads(bibtex)
    bibtex_entries = [BibTexEntry(entry) for entry in bib_db.entries]
    return bibtex_entries
