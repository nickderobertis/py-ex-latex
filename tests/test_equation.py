import pyexlatex as pl

EQUATION_STR = r'a_b = \sum_{d=0}^{D} \frac{C^{de}}{f}'
EQUATION_TEMPLATE = """
Some inline text {{ eq | Equation }}. Offset eq: {{ eq | Equation(inline=False) }} Yes.
"""

EXPECT_INLINE_EQ = '$a_b = \\sum_{d=0}^{D} \\frac{C^{de}}{f}$'
EXPECT_OFFSET_EQ = '\\begin{equation}\n\ta_b = \\sum_{d=0}^{D} \\frac{C^{de}}{f}\n\\end{equation}'
EXPECT_TEMPLATE_OUTPUT = '\nSome inline text $a_b = \\sum_{d=0}^{D} \\frac{C^{de}}{f}$. Offset eq: \\begin{equation}\n\ta_b = \\sum_{d=0}^{D} \\frac{C^{de}}{f}\n\\end{equation} Yes.'


def test_inline_equation():
    eq = pl.Equation(str_eq=EQUATION_STR)
    assert str(eq) == EXPECT_INLINE_EQ
    eq = pl.Equation(EQUATION_STR)
    assert str(eq) == EXPECT_INLINE_EQ


def test_offset_equation():
    eq = pl.Equation(str_eq=EQUATION_STR, inline=False)
    assert str(eq) == EXPECT_OFFSET_EQ
    eq = pl.Equation(EQUATION_STR, inline=False)
    assert str(eq) == EXPECT_OFFSET_EQ


def test_equations_in_template():
    class MyModel(pl.Model):
        eq = EQUATION_STR

    mod = MyModel(template_str=EQUATION_TEMPLATE)
    assert str(mod) == EXPECT_TEMPLATE_OUTPUT
