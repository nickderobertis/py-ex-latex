from sympy import Eq, symbols
import pyexlatex as pl

STR_EQ = r'a = b^{2} + \frac{c}{d}'
a, b, c, d = symbols('a b c d')
SYMPY_EQ = Eq(a, b ** 2 + c/d)


def test_eq_inline():
    eq_from_str = pl.Equation(str_eq=STR_EQ)
    eq_from_sympy = pl.Equation(eq=SYMPY_EQ)

    assert str(eq_from_str) == str(eq_from_sympy) == f'${STR_EQ}$'


def test_eq_offset_numbered():
    eq_from_str = pl.Equation(str_eq=STR_EQ, inline=False, numbered=True)
    eq_from_sympy = pl.Equation(eq=SYMPY_EQ, inline=False, numbered=True)

    assert str(eq_from_str) == str(eq_from_sympy) == '\\begin{equation}\n\t' + STR_EQ + '\n\\end{equation}'


def test_eq_offset_no_numbers():
    eq_from_str = pl.Equation(str_eq=STR_EQ, inline=False, numbered=False)
    eq_from_sympy = pl.Equation(eq=SYMPY_EQ, inline=False, numbered=False)

    assert str(eq_from_str) == str(eq_from_sympy) == f'\n$${STR_EQ}$$\n'
