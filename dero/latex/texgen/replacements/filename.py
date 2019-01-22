def latex_filename_replacements(string):
    return string.replace('%', 'pct').replace('/','_').replace('\\','_').replace('-','_').replace('$','')