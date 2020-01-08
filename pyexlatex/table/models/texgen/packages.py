from pyexlatex.models.package import Package
from pyexlatex.texgen.packages.columntypes import ColumnTypesPackage

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
]

default_packages = [Package(package_str) for package_str in _default_package_strs] + _direct_default_packages  # type: ignore