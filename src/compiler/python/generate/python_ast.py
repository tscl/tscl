"""
Generate Python 3 AST
"""
import ast as python
from functools import singledispatch

from lib import AST as tscl

__all__ = [
    'generate',
]


@singledispatch
def generate(node):
    raise NotImplementedError('Python AST Generation Error: %r' % node)


# root

@generate.register(tscl.Program)
def _(node) -> "python.Expression":
    """
    Transform a tscl AST into an compilable Python AST.
    """
    return python.fix_missing_locations(
        python.Module(
            body=[expr(generate(node)) for node in node.expressions],
            lineno=1,
            col_offset=1,
        )
    )


# values

@generate.register(tscl.Integer)
def _(node):
    return python.Num(
        n=int(node.value),
        lineno=1,
        col_offset=1,
    )


@generate.register(tscl.Float)
def _(node):
    return python.Num(
        n=float(node.value),
        lineno=1,
        col_offset=1,
    )


@generate.register(tscl.List)
def _(node):
    return python.List(
        elts=[generate(node) for node in node.expressions],
        ctx=python.Load(),
        lineno=1,
        col_offset=1,
    )


# helpers

def expr(node):
    return python.Expr(
        value=node,
        lineno=1,
        col_offset=1,
    )


def p(message):
    return expr(
        python.Call(
            func=python.Name(id='print', ctx=python.Load()), args=[
                python.Str(s=message)
            ], keywords=[], starargs=None, kwargs=None
        )
    )
