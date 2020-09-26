from sympy import Eq, Expr, Symbol
from sympy import latex


def inline(eq: Eq) -> str:
    return f'${latex(eq)}$'


def offset(eq: Eq) -> str:
    return f'\\begin{{equation}}\n\t{latex(eq)}\n\\end{{equation}}'


def offset_no_numbering(eq: Eq) -> str:
    return f'\n$${latex(eq)}$$\n'


def latex_partial(expr: Expr, eq_symbol: Symbol, wrt_symbol: Symbol, offset: bool = False) -> str:

    begin_str = '$'
    end_str = '$'
    if offset:
        begin_str = '\\begin{equation}\n\t'
        end_str = '\n\\end{equation}'
    return rf'{begin_str}\frac{{\partial {latex(eq_symbol)}}}{{\partial {latex(wrt_symbol)}}} = ' \
        rf'{latex(expr)}{end_str}'
