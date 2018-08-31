from dero.latex.models.package import Package

simple_package_strs = [
    'caption',
    'subcaption',
    'graphicx',
    'pdflscape'
]
simple_packages = [Package(str_) for str_ in simple_package_strs]

default_packages = simple_packages + []  # add any packages with options here with the Package class