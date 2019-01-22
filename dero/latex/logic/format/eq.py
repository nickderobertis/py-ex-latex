from sympy import Eq, latex


def inline(eq: Eq) -> str:
    return f'${latex(eq)}$'


def offset(eq: Eq) -> str:
    return f'$${latex(eq)}$$'
