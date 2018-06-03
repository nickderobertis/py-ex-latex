from dero.latex.models.package import Package
from dero.latex.table.models.texgen.newcolumntype import NewColumnTypes

_default_package_strs = [
    'amsmath',
    'pdflscape',
    'dcolumn',
    'booktabs',
    'array',
    'threeparttable'
]

_direct_default_packages = [
    Package('geometry', modifier_str='margin=0.3in')
]

default_packages = [Package(package_str) for package_str in _default_package_strs] + \
                   _direct_default_packages + [NewColumnTypes()]