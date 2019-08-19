from pyexlatex.models.package import Package

simple_package_strs = [
    'caption',
    'subcaption',
    'graphicx',
    'pdflscape',
    'fancyhdr',
    'lastpage',
    'textcomp'
]
simple_packages = [Package(str_) for str_ in simple_package_strs]

direct_packages = [
    
]

default_packages = simple_packages + direct_packages  # add any packages with options here with the Package class