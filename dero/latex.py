
import os, datetime, filecmp, shutil, math
import pandas as pd
from io import StringIO

from .data import replace_missing_csv


def date_time_move_latex(tablename,filepath, folder_name='Tables'):
    r"""
    Takes a LaTeX tex and PDF after the PDF's been created by pdflatex and moves it into a table
    folder with the date, checking if the table was just previously created. If it's the same as
    before, it just deletes the file.

    Required arguments:
        tablename: operating system name of the table, without extensions
        filepath: full filepath of table, without table name. put r before quotes as follows: r'C:\Users\Folder'

    """
    def exit_sequence(tablename, filepath):
        os.remove(os.path.join(filepath, str(tablename) + '.aux'))
        os.remove(os.path.join(filepath, str(tablename) + '.log'))
        return

    os.chdir(filepath) #sets working directory to current directory of table
    table_pdf = tablename + ".pdf"
    table_tex = tablename + ".tex"
    table_xlsx = tablename + ".xlsx"
    inpath_pdf = os.path.join(filepath,table_pdf)
    inpath_tex = os.path.join(filepath,table_tex)
    inpath_xlsx = os.path.join(filepath,table_xlsx)

    tables_path = os.path.join(filepath, folder_name) #set table directory
    if not os.path.exists(tables_path): #create a general table directory if it doesn't exist
        os.makedirs(tables_path)

    current_date = datetime.datetime.today().timetuple()
    current_time = datetime.datetime.today().timetuple()
    format_time = [str(current_time[0]),str(current_time[1]),str(current_time[2])]
    for i in range(3):
        if current_time[i] < 10:
            format_time[i] = "0" + str(current_time[i])
    datetime_str = "{}-{}-{}_".format(format_time[0],format_time[1],format_time[2])

    count = 0 #set up count variable
    while True: #continuous loop
        count += 1
        str_count = "Num" + str(count)
        name_str = datetime_str + str_count
        folder_path = os.path.join(tables_path,name_str)
        outpath_tex = os.path.join(folder_path,table_tex)
        outpath_pdf = os.path.join(folder_path,table_pdf)
        outpath_xlsx = os.path.join(folder_path,table_xlsx)
        if os.path.exists(folder_path): #if the folder already exists
            if os.path.exists(outpath_tex): #if there is already a tex file with the same name
                if filecmp.cmp(outpath_tex,inpath_tex) == True: #if this is the same exact table
                    exit_sequence(tablename,filepath)
                    os.remove(inpath_pdf)
                    os.remove(inpath_tex)
                    if os.path.isfile(inpath_xlsx): #if there is an XLSX file, delete it as well
                        os.remove(inpath_xlsx)
                    return #stop
                else: #if there is a tex file with the same name but it's not the same table
                    continue #go to next iteration of loop (change output number)
            else:
                shutil.move(inpath_pdf,outpath_pdf) #moves file
                shutil.move(inpath_tex,outpath_tex) #moves file
                if os.path.isfile(inpath_xlsx): #if Excel file exists, move it
                    shutil.move(inpath_xlsx,outpath_xlsx)
                exit_sequence(tablename,filepath)
                return
        else: #if the folder doesn't exist
            os.mkdir(folder_path) #create the folder
            shutil.move(inpath_pdf,outpath_pdf) #moves file
            shutil.move(inpath_tex,outpath_tex) #moves file
            if os.path.isfile(inpath_xlsx): #if Excel file exists, move it
                    print(inpath_xlsx)
                    print(outpath_xlsx)
                    shutil.move(inpath_xlsx,outpath_xlsx)
            exit_sequence(tablename,filepath)
            return
        
def csv_to_raw_latex(infile, csvstring=False, missing_rep=" - ", formatstr='{:.3f}', skipfix=None):
    '''
    Takes a CSV text file and converts it to a LaTeX formatted list, with each line of the LaTeX
    file as an item in the list.
    
    Required options:
        infile: Full file path of CSV (include r before quotes)
    
    Optional options:
        csvstring: True to pass a CSV string to infile rather than load from file
        missing_rep: Representation for missing numbers, default " - "
        formatstr: Python string for number formatting, for example '{:.3f}' with quotes
        skipfix: String or list of strings of fixes to skip, options are ['&','%','_']
    '''
    latex_list = []
    if not csvstring:
        f = open(infile,'r')
    else:
        from io import StringIO
        f = StringIO(infile)
        
    if skipfix:
        if isinstance(skipfix, str):
            skipfix = [skipfix]
        assert isinstance(skipfix, list)
    
    csv_list = f.readlines()
    miss_csv_list = replace_missing_csv(csv_list,missing_rep)
    latex_list = []
    for i, line in enumerate(miss_csv_list):
        line_string = ''
        for j, item in enumerate(line):
            if j is not 0: #don't put an & before the first item in line
                line_string += ' & '
            #LaTeX character fixes
            if skipfix:
                if '&' not in skipfix:
                    item = item.replace('&', '\&')
                if '%' not in skipfix:
                    item = item.replace('%', '\%')
                if '_' not in skipfix:
                    item = item.replace('_', '\_')
            else: #make all replacements
                item = item.replace('&','\&')
                item = item.replace('%','\%')
                item = item.replace('_','\_')
            if item.find('.') is not -1: #if we are dealing with a number with decimals
                try:
                    item = formatstr.format(float(item))
                except:
                    pass
            item = item.replace('\n','')
            line_string += item
        line_string += " \\\ \n"
        if i is 0: #on the first line, remove quotes from names
            line_string = line_string.replace('''"''','') #strip out quotes
        latex_list.append(line_string)
        
    if not csvstring:
        f.close()
        
    return latex_list

def df_to_pdf_and_move(dflist, outfolder, outname='table', tabular_string='', string_format='{:.3f}', 
                       above_text='', below_text='',
                     font_size=12, caption='', parse_dates=False, missing_rep=' - ', panel_names=None, colname_flags=None,
                      outmethod='pandas'):
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
        string_format:  String or list of format of numbers in the table. Please see Python number formats. {:.3f} is 
                        three decimals, the default.
        font_size:      Font size, default 12
        caption:        Title of table
        missing_rep:    Representation for missing numbers, default " - "
        panel_names:    Python list of names of each panel, to go below column names, e.g. ['Table','Other Table']
        colname_flags:  Python list of yes or no flags for whether to display column names for each panel. Default is to
                        display column names only for the first panel, as usually the panels have the same columns. 
                        The default input for a three panel table would be ['y','n','n']
        outmethod:      String, 'pandas' or 'csv'. If 'pandas', uses pandas' built in df.to_latex() to build latex. If
                        'csv', uses df.to_csv() and then dero.raw_csv_to_latex(). The latter case is useful when the table
                        itself contains latex expressions.
    
    '''   
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

    outname_tex = str(outname) + ".tex"
    outname_pdf = str(outname) + ".pdf"
    outpath = os.path.join(outfolder, outname_tex)
    latex_string_list = [] #set container for final LaTeX table contents
    if (colname_flags is None) or (len(colname_flags) is not len(dflist)): #if the user didn't specify whether to use colnames, or they specified an incorrect number of flags
        colname_flags = ['y'] #set first colnames to show
        for i in range(len(dflist) - 1):
            colname_flags.append('n') #set rest of colnames not to show
    for i, df in enumerate(dflist): #for each csv in the list
        df = dflist[i].applymap(lambda x: string_format[i].format(float(x)) if is_number(x) else x)
        df = df.fillna(missing_rep)
        if outmethod.lower() == 'pandas':
            latex_list = [line for line in df.to_latex().split('\n') if not line.startswith('\\')]
        elif outmethod.lower() == 'csv':
            latex_list = [line for line in csv_to_raw_latex(df.to_csv(), missing_rep=missing_rep,
                                                        csvstring=True, skipfix='_') if not line.startswith('\\')]
        number_of_columns = 1 + latex_list[0].count(' & ') #number of columns is 1 + number of seperators
        if panel_names is not None:
            panel_letter = chr(i + ord('A')) #sets first panel to A, second to B, and so on
            #LaTeX formatting code
            latex_list.insert(1,r'\midrule \\[-11pt]')
            latex_list.insert(2,'\n')
            latex_list.insert(3,r'\multicolumn{' + str(number_of_columns) + '}{c}{Panel '+ panel_letter + ': ' + panel_names[i] + '} \\\ \\\[-11pt]')
            latex_list.insert(4,'\n')
            latex_list.insert(5,r'\midrule')
            latex_list.insert(6,'\n')
        else: #if there is no panel name, just put in a midrule
            latex_list.insert(1,r'\midrule')
            latex_list.insert(2,'\n')
        if colname_flags[i].lower() in ('n','no'): #if the flag for colnames is no for this panel
            latex_list = latex_list[1:] #chop off colnames
        latex_string = "\n".join(latex_list) #convert list to string
        latex_string_list.append(latex_string) #add this csv's LaTeX table string to the full list of LaTeX table strings


    if tabular_string == "": #set default tabular format
        tabular_string = 'l' + 'c' * (number_of_columns - 1) #first column left aligned, rest centered
    
    #Set list of lines to be written to output file at beginning
    latex_header_list = [r'\documentclass[' + str(font_size) + 'pt]{article}',r'\usepackage{amsmath}',r'\usepackage{pdflscape}',r'\usepackage[margin=0.3in]{geometry}',
                         r'\usepackage{dcolumn}',r'\usepackage{booktabs}',r'\usepackage{array}', r'\usepackage{threeparttable}',
                         r'\newcolumntype{L}[1]{>{\raggedright\let\newline\\\arraybackslash\hspace{0pt}}m{#1}}',
                         r'\newcolumntype{C}[1]{>{\centering\let\newline\\\arraybackslash\hspace{0pt}}m{#1}}',
                         r'\newcolumntype{R}[1]{>{\raggedleft\let\newline\\\arraybackslash\hspace{0pt}}m{#1}}',
                         r'\newcolumntype{.}{D{.}{.}{-1}}',r'\title{\LaTeX}',r'\date{}',r'\author{Nick DeRobertis}',
                         r'\begin{document}',r'\begin{table}',r'\centering',r'\begin{threeparttable}',
                         above_text,r'\caption{' + caption + '}',r'\begin{tabular}{' + tabular_string + '}',
                         r'\toprule']

    #Set list of lines to be written to output file at end
    latex_footer_list = [r'\bottomrule',r'\end{tabular}',r'\begin{tablenotes}[para,flushleft]',r'\item ' + below_text,r'\end{tablenotes}',r'\end{threeparttable}',r'\end{table}',r'\end{document}']

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
    os.system('pdflatex ' + '"' + outname_tex + '"') #create PDF
    date_time_move_latex(outname,outfolder) #move table into appropriate date/number folder
    
def latex_equations_to_pdf(latex_list, directory, name='Equations', below_text=None,
                           math_size=18, text_size=14, title=None, para_space='1em',
                          inline=False):
    script_size = math.ceil(math_size * (2/3))
    scriptscript_size = math.ceil(math_size * .5)
    assert text_size in (8, 9, 10, 11, 12, 14, 17, 20) #latex allowed font sizes
    
    if inline:
        surround_char_beg = '$'
        surround_char_end = '$'
    else:
        surround_char_beg = r'\begin{dmath}'
        surround_char_end = r'\end{dmath}'

    
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
    with open(file_path, 'w') as f:
        f.write('\n'.join(headers) + '\n')
        [f.write(surround_char_beg + '{}'.format(line) + surround_char_end + '\n\n') for line in latex_list]
        if below_text:
            f.write('\n' + below_text + '\n')
        f.write('\n'.join(footers))
        
    os.chdir(directory)
    os.system('pdflatex ' + '"' + name_tex + '"') #create pdf
    date_time_move_latex(name, directory, 'Equations')