import os

import pandas as pd

from pyexlatex.tools import csv_to_raw_latex, date_time_move_latex


def df_to_pdf_and_move(dflist, outfolder, outname='table', tabular_string='', string_format='',
                       above_text='', below_text='',
                     font_size=12, caption='', missing_rep=' - ', landscape=False,
                       panel_names=None, colname_flags=None,
                       as_document=True, outmethod='pandas'):
    '''
    Takes a dataframe or list of dataframes as input and outputs to a LaTeX formatted table with multiple panels,
    creates a PDF, and moves the LaTeX file and PDF to a dated folder.

    Required options:
        dflist:         Dataframe or list of dataframes.
        outfolder:      Output folder for LaTeX file and PDF. Inside of this folder, a folder called Tables will be created,
                        inside of which the two files will be put inside another folder with the date.


    Optional options:
        outname:        Name of output table, default is table
        tabular_string: Can take any string that would normally used in tabular (i.e. rrr for three columns right aligned
                        as well as L{<width>), C{<width>}, and R{<width>} (i.e. L{3cm}) for left, center, and right aligned
                        fixed width. Additionally . aligns on the decimal. Default is first column left aligned, rest
                        center aligned.
        string_format:  String or list of format of numbers in the table. Please see Python number formats. Pass a blank
                        string to leave formatting untouched (the default).
        above_text:     String of text to display above table
        below_text:     String of text to display below table
        font_size:      Font size, default 12
        caption:        Title of table
        missing_rep:    Representation for missing numbers, default " - "
        landscape:      Boolean. True to switch table to landscape output instead of portrait.
        panel_names:    Python list of names of each panel, to go below column names, e.g. ['Table','Other Table']
        colname_flags:  Python list of yes or no flags for whether to display column names for each panel. Default is to
                        display column names only for the first panel, as usually the panels have the same columns.
                        The default input for a three panel table would be ['y','n','n']
        as_document:    Boolean. True to output latex wrappers for table to be a standalone document. False to write
                        only table wrappers so that table can be included in another document
        outmethod:      String, 'pandas' or 'csv'. If 'pandas', uses pandas' built in df.to_latex() to build latex. If
                        'csv', uses df.to_csv() and then pyexlatex.df.raw_csv_to_latex(). The latter case is useful when the table
                        itself contains latex expressions.

    '''
    from pyexlatex.texgen.replacements.file import general_latex_replacements

    if isinstance(dflist, pd.DataFrame):
        dflist = [dflist]
    assert isinstance(dflist, list)
    if isinstance(string_format, str):
        string_format = [string_format] * len(dflist)
    assert isinstance(string_format, list)

    def is_number(s):
        try:
            float(s)
            return True
        except (ValueError, TypeError):
            return False

    def latex_filename_replacements(string):
        return string.replace('%', 'pct').replace('/','_').replace('\\','_')

    def all_latex_replacements(*tuple):
        return [general_latex_replacements(item) for item in tuple]

    # Latex string replacements will be made in the data below. Here make adjustments to titles, above/below text, etc.
    caption, above_text, below_text = all_latex_replacements(caption, above_text, below_text)
    outname = latex_filename_replacements(outname)
    if panel_names is not None:
        panel_names = all_latex_replacements(*panel_names)

    outname_tex = str(outname) + ".tex"
    outpath = os.path.join(outfolder, outname_tex)
    latex_string_list = [] #set container for final LaTeX table contents
    if (colname_flags is None) or (len(colname_flags) is not len(dflist)): #if the user didn't specify whether to use colnames, or they specified an incorrect number of flags
        colname_flags = ['y'] #set first colnames to show
        for i in range(len(dflist) - 1):
            colname_flags.append('n') #set rest of colnames not to show
    panel_order = -1
    for i, df in enumerate(dflist): #for each csv in the list
        if string_format[i]:
            df = dflist[i].applymap(lambda x: string_format[i].format(float(x)) if is_number(x) else x)
        df = df.fillna(missing_rep)
        if outmethod.lower() == 'pandas':
            latex_list = [line for line in df.to_latex().split('\n') if not line.startswith('\\')]
        elif outmethod.lower() == 'csv':
            latex_list = [line for line in csv_to_raw_latex(df.to_csv(), missing_rep=missing_rep,
                                                            csvstring=True, skipfix='_',
                                                            formatstr=string_format[i]) if not line.startswith('\\')]
        number_of_columns = 1 + latex_list[0].count(' & ') #number of columns is 1 + number of seperators
        if colname_flags[i].lower() in ('n','no'): #if the flag for colnames is no for this panel
            latex_list = latex_list[1:] #chop off colnames
        if panel_names is not None and panel_names[i]:
            panel_order += 1 #In combination with next line, sets panel to A, etc.
            panel_letter = chr(panel_order + ord('A')) #sets first panel to A, second to B, and so on
            #LaTeX formatting code
            panel_latex_list = [
                r'\midrule \\[-11pt]',
                '\n',
                r'\multicolumn{' + str(number_of_columns) + '}{c}{Panel '+ panel_letter + ': ' + panel_names[i] + '} \\\ \\\[-11pt]',
                '\n',
                r'\midrule',
                '\n'
            ]
        else: #if there is no panel name, just put in a midrule
            panel_latex_list = [
                r'\midrule',
                '\n'
            ]
        latex_list = panel_latex_list + latex_list
        latex_string = "\n".join(latex_list) #convert list to string
        latex_string_list.append(latex_string) #add this csv's LaTeX table string to the full list of LaTeX table strings


    if tabular_string == "": #set default tabular format
        tabular_string = 'l' + 'c' * (number_of_columns - 1) #first column left aligned, rest centered

    #Set list of lines to be written to output file at beginning
    document_header_list = [r'\documentclass[' + str(font_size) + 'pt]{article}',r'\usepackage{amsmath}',r'\usepackage{pdflscape}',r'\usepackage[margin=0.3in]{geometry}',
                         r'\usepackage{dcolumn}',r'\usepackage{booktabs}',r'\usepackage{array}', r'\usepackage{threeparttable}',
                         r'\newcolumntype{L}[1]{>{\raggedright\let\newline\\\arraybackslash\hspace{0pt}}m{#1}}',
                         r'\newcolumntype{C}[1]{>{\centering\let\newline\\\arraybackslash\hspace{0pt}}m{#1}}',
                         r'\newcolumntype{R}[1]{>{\raggedleft\let\newline\\\arraybackslash\hspace{0pt}}m{#1}}',
                         r'\newcolumntype{.}{D{.}{.}{-1}}',r'\title{\LaTeX}',r'\date{}',r'\author{Nick DeRobertis}',
                         r'\begin{document}']

    table_header_list =  [r'\begin{table}',r'\centering',r'\begin{threeparttable}',
                         above_text,r'\caption{' + caption + '}',r'\begin{tabular}{' + tabular_string + '}',
                         r'\toprule']

    #Set list of lines to be written to output file at end
    table_footer_list = [r'\bottomrule',r'\end{tabular}',r'\begin{tablenotes}[para,flushleft]',r'\item ' + below_text,r'\end{tablenotes}',
                         r'\end{threeparttable}',r'\end{table}']

    document_footer_list = [r'\end{document}']

    if landscape:
        table_header_list.insert(0, r'\begin{landscape}')
        table_footer_list.append(r'\end{landscape}')

    if as_document:
        latex_header_list = document_header_list + table_header_list
        latex_footer_list = table_footer_list + document_footer_list
    else:
        latex_header_list = table_header_list
        latex_footer_list = table_footer_list

    #Actually write to file
    with open(outpath,'w') as f:
        for line in latex_header_list: #write each line in the header list, with carriage returns in between
            f.write(line)
            f.write("\n")
        for latex_string in latex_string_list: #write each csv table to file in LaTeX format
            f.write(latex_string)
        for line in latex_footer_list: #write each line in the footer list, with carriage returns in between
            f.write(line)
            f.write("\n")
        f.close()


    os.chdir(outfolder) #changes working filepath
    # Only create pdf if we are creating a standalone document
    if as_document:
        os.system('pdflatex ' + '"' + outname_tex + '"') #create PDF
    date_time_move_latex(outname, outfolder) #move table into appropriate date/number folder