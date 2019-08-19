import math
import os

from pyexlatex.tools import date_time_move_latex


def latex_equations_to_pdf(latex_list, directory, name='Equations', below_text=None,
                           math_size=18, text_size=14, title=None, para_space='1em',
                          inline=False, as_document=True):
    script_size = math.ceil(math_size * (2/3))
    scriptscript_size = math.ceil(math_size * .5)
    assert text_size in (8, 9, 10, 11, 12, 14, 17, 20) #latex allowed font sizes

    if inline:
        surround_char_beg = '$'
        surround_char_end = '$'
    else:
        surround_char_beg = r'\begin{dmath}'
        surround_char_end = r'\end{dmath}'

    # Header and footer are needed to create a standalone document using the equations.
    # If as_document=False, header and footer will not be used.
    headers = [r'\documentclass[{} pt]{{extarticle}}'.format(text_size),
               #First size is text size, second is math size, third is script size,
               #fourth is scriptscript size
               r'\DeclareMathSizes{{{0}}}{{{1}}}{{{2}}}{{{3}}}'.format(
                    text_size, math_size, script_size, scriptscript_size),
               r'\usepackage{amsmath}',
               r'\usepackage{breqn}',
               r'\usepackage[margin=0.3in]{geometry}',
              r'\author{Nick DeRobertis}' ,r'\begin{document}', r'\setlength{{\parskip}}{{{}}}'.format(para_space)]
    footers = [r'\end{document}']

    name_tex = name + '.tex'
    file_path = os.path.join(directory, name_tex)

    # Actually write to file
    with open(file_path, 'w') as f:
        if as_document:
            f.write('\n'.join(headers) + '\n')
        [f.write(surround_char_beg + '{}'.format(line) + surround_char_end + '\n\n') for line in latex_list]
        if below_text:
            f.write('\n' + below_text + '\n')
        if as_document:
            f.write('\n'.join(footers))

    os.chdir(directory)
    # Only create pdf if we are creating a standalone document
    if as_document:
        os.system('pdflatex ' + '"' + name_tex + '"') #create pdf
    date_time_move_latex(name, directory, 'Equations')