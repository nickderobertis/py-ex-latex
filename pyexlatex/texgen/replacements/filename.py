import os


def latex_filename_replacements(string):
    return string.replace('%', 'pct').replace('/','_').replace('\\','_').replace('-','_').replace('$','')


def _latex_valid_basename(filepath):
    basename = os.path.basename(filepath)
    return basename.replace(' ', '_').replace('/','_').replace('%','pct').replace('$','')