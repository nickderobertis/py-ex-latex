from pyexlatex.models.environmenttemplate import EnvironmentTemplate


class NoPageBreak(EnvironmentTemplate):
    """
    Contents within this environment will not have a page break come in the middle. Contents will instead be moved
    onto the next page if a break would have occurred.
    """
    name = 'absolutelynopagebreak'

    # taken from https://tex.stackexchange.com/a/94702
    begin_def = r'\par\nobreak\vfil\penalty0\vfilneg\vtop\bgroup'
    end_def = r'\par\xdef\tpd{\the\prevdepth}\egroup\prevdepth=\tpd'