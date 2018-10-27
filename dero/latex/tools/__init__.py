import datetime
import filecmp
import os
import shutil

from dero.data import replace_missing_csv


def date_time_move_latex(tablename,filepath, folder_name='Tables'):
    r"""
    Takes a LaTeX tex and PDF after the PDF's been created by pdflatex and moves it into a table
    folder with the date, checking if the table was just previously created. If it's the same as
    before, it just deletes the file.

    Required arguments:
        tablename: operating system name of the table, without extensions
        filepath: full filepath of table, without table name. put r before quotes as follows: r'C:\Users\Folder'

    """
    def remove_if_exists(filepath):
        try:
            os.remove(filepath)
        except FileNotFoundError:
            print('Cannot delete: did not find {}'.format(filepath))

    def move_if_exists(inpath, outpath):
        try:
            shutil.move(inpath, outpath)
        except FileNotFoundError:
            print('Cannot move: did not find {}'.format(inpath))

    def remove_all_if_exist(filepaths):
        [remove_if_exists(filepath) for filepath in filepaths]

    def move_all_if_exists(inpaths, outfolder):
        [move_if_exists(inpath, outfolder) for inpath in inpaths]

    def exit_sequence():
        inpath_aux = os.path.join(filepath, str(tablename) + '.aux')
        inpath_log = os.path.join(filepath, str(tablename) + '.log')
        remove_all_if_exist([inpath_aux, inpath_log])
        return

    os.chdir(filepath) #sets working directory to current directory of table
    table_pdf = tablename + ".pdf"
    table_tex = tablename + ".tex"
    table_xlsx = tablename + ".xlsx"
    inpath_pdf = os.path.join(filepath,table_pdf)
    inpath_tex = os.path.join(filepath,table_tex)
    inpath_xlsx = os.path.join(filepath,table_xlsx)
    all_inpaths = [inpath_pdf, inpath_tex, inpath_xlsx]

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
        outpath_tex =  os.path.join(folder_path, table_tex)
        if os.path.exists(folder_path): #if the folder already exists
            if os.path.exists(outpath_tex): #if there is already a tex file with the same name
                if filecmp.cmp(outpath_tex,inpath_tex) == True: #if this is the same exact table
                    exit_sequence()
                    remove_all_if_exist(all_inpaths)
                    return None
                else: #if there is a tex file with the same name but it's not the same table
                    continue #go to next iteration of loop (change output number)
            else:
                move_all_if_exists(all_inpaths, folder_path)
                exit_sequence()
                return folder_path
        else: #if the folder doesn't exist
            os.mkdir(folder_path) #create the folder
            move_all_if_exists(all_inpaths, folder_path)
            exit_sequence()
            return folder_path


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
                if formatstr:
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