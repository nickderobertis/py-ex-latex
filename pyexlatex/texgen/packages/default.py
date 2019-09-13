from pyexlatex.figure.packages import default_packages as default_figure_packages
from pyexlatex.table.models.texgen.packages import default_packages as default_table_packages

# exclude geometry package as has different margins in figure vs table. Use table default.
figure_packages = [package for package in default_figure_packages if not package.matches_name('geometry')]
default_packages = list(set(default_table_packages + figure_packages))