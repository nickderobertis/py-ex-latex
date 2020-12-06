from sympy import Eq, Expr, Symbol
from sympy import latex


def inline(eq: str) -> str:
    return f'${eq}$'


def offset(eq: str) -> str:
    return f'\\begin{{equation}}\n\t{eq}\n\\end{{equation}}'


def offset_no_numbering(eq: str) -> str:
    return f'\n$${eq}$$\n'


def latex_partial(expr: Expr, eq_symbol: Symbol, wrt_symbol: Symbol, offset: bool = False) -> str:

    begin_str = '$'
    end_str = '$'
    if offset:
        begin_str = '\\begin{equation}\n\t'
        end_str = '\n\\end{equation}'
    return rf'{begin_str}\frac{{\partial {latex(eq_symbol)}}}{{\partial {latex(wrt_symbol)}}} = ' \
        rf'{latex(expr)}{end_str}'
