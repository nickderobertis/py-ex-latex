from dero.latex.models.package import Package
from dero.latex.texgen.packages.columntypes import ColumnTypesPackage

_default_package_strs = [
    'amsmath',
    'pdflscape',
    'booktabs',
    'array',
    'threeparttable',
    'fancyhdr',
    'lastpage',
    'textcomp'
]

_direct_default_packages = [
    ColumnTypesPackage(),
    Package('fontenc', modifier_str='T1'),  # allows printing of > and <
    Package('biblatex', modifier_str='backend=bibtex,citestyle=authoryear,natbib')
]

default_packages = [Package(package_str) for package_str in _default_package_strs] + _direct_default_packages