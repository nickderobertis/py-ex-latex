import pyexlatex.resume as lr
import pyexlatex as pl
from tests.base import GENERATED_FILES_DIR
from tests.utils.pdf import compare_pdfs_in_generated_vs_input_by_name

JOB_CONTENTS = pl.UnorderedList(['I did', 'some things', 'today'])
JOB = lr.Employment(JOB_CONTENTS, 'Company Name', '2015 - Present', 'Job Title', 'Location, Here', extra_contents='Extra contents')
EDUCATION = lr.Education('Some School', 'Location, Here', 'Bachelor of Science in Something', 'May 2020', '4.0/4.0')
PUBLICATION = lr.Publication(
    'Publication Title',
    ['Coauthor One', 'Coauthor Two'],
    journal_info='Journal of Awesome',
    href='https://www.example.com/',
    extra_info='This was a really neat paper',
    description='A description of the paper'
)
REFERENCE = lr.Reference('My Reference', title_lines=['Reference Title', 'Can be Multiple Lines'],
                         company='Organization', contact_lines=['Address', 'Phone', 'Whatever contact'],
                         email='abc@123.com')
AWARD = lr.Award('Cool Award', 'May 2020', 'Some extra info')
CONTACT_LINES = [
    ['Nick DeRobertis'],
    ['Location, here'],
    ['Contact 1', 'Contact 2']
]

def test_basic_resume():
    contents = [
        pl.Section(
            [
                'An overview'
            ],
            title='Normal section'
        ),
        lr.SpacedSection(
            [
                JOB,
                EDUCATION,
                PUBLICATION,
                AWARD,
                REFERENCE
            ],
            title='Spaced Section'
        )
    ]
    doc = lr.Resume(
        contents,
        contact_lines=CONTACT_LINES
    )
    assert str(doc) == '\\documentclass[11pt]{resume}\n\\newenvironment{absolutelynopagebreak}{\\par\\nobreak\\vfil\\penalty0\\vfilneg\\vtop\\bgroup}{\\par\\xdef\\tpd{\\the\\prevdepth}\\egroup\\prevdepth=\\tpd}\n\\usepackage[left=0.75in,top=0.6in,right=0.75in,bottom=0.6in]{geometry}\n\\usepackage{xcolor}\n\\definecolor{darkblue}{RGB}{50,82,209}\n\\usepackage[hidelinks]{hyperref}\n\\usepackage{ragged2e}\n\\address{Nick DeRobertis}\n\\address{Location, here}\n\\address{Contact 1 \\\\ Contact 2}\n\\begin{document}\n\\begin{section}{Normal section}\nAn overview\n\\end{section}\n\\begin{section}{Spaced Section}\n\\vspace{0.2cm}\n\\begin{absolutelynopagebreak}\n\\begin{employment}{Company Name}{2015 - Present}{Job Title}{Location, Here}\n\\item \\begin{itemize}\n\\item I did\n\\item some things\n\\item today\n\\end{itemize}\nExtra contents\n\\end{employment}\n\\end{absolutelynopagebreak}\n\n\\begin{absolutelynopagebreak}\n\\textbf{Some School}\n (GPA 4.0/4.0)\n\\hfill\n\\textbf{May 2020}\n\\\\\n\\textit{Bachelor of Science in Something}\n\\hfill\nLocation, Here\n\\\\[-8pt]\n\\end{absolutelynopagebreak}\n\n\\begin{absolutelynopagebreak}\n\\hangindent=1cm\n\\href{https://www.example.com/}{\\underline{\\textcolor{darkblue}{Publication Title}}},\n\\textit{Journal of Awesome}\n with \nCoauthor One\n and \nCoauthor Two\nThis was a really neat paper\n\n\\justifying\nA description of the paper\n\\vspace{0.2cm}\n\\vspace{0.2cm}\n\\end{absolutelynopagebreak}\n\n\\begin{absolutelynopagebreak}\n\\textbf{Cool Award}\n (Some extra info)\n\\hfill\nMay 2020\n\\\\[-8pt]\n\\end{absolutelynopagebreak}\n\n\\begin{absolutelynopagebreak}\n\\textsc{\\textbf{My Reference}}\n\\\\\n\\textit{Reference Title}\n\\\\\n\\textit{Can be Multiple Lines}\n\\\\\nOrganization\n\\\\\nAddress\n\\\\\nPhone\n\\\\\nWhatever contact\n\\\\\nabc@123.com\n\\\\\n\\\\[-8pt]\n\\end{absolutelynopagebreak}\n\\vspace{-0.2cm}\n\\end{section}\n\\end{document}'
    name = 'resume basic'
    doc.to_pdf(outfolder=GENERATED_FILES_DIR, outname=name)
    compare_pdfs_in_generated_vs_input_by_name(name)
