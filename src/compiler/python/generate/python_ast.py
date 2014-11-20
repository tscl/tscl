"""
Generate Python 3 AST
"""
import ast as python
from functools import singledispatch

from lib import AST as tscl
from generate import name_generator

__all__ = [
    'generate',
]


@singledispatch
def generate(node, inline) -> "python.*":
    """
    Recursively transform a tscl AST into an compilable Python AST.
    """
    raise NotImplementedError('Python AST Generation Error: generate(%r, %r)' % (node, inline))


# root

@generate.register(tscl.Program)
def _(node) -> "python.Expression":
    inline = []
    return python.fix_missing_locations(
        python.Module(
            body=inline+[expr(generate(node, inline)) for node in node.expressions],
        )
    )


# values

@generate.register(tscl.Integer)
def _(node, inline):
    return python.Num(
        n=int(node.value),
    )


@generate.register(tscl.Float)
def _(node, inline):
    return python.Num(
        n=float(node.value),
    )


@generate.register(tscl.List)
def _(node, inline):
    return python.List(
        elts=[generate(node, inline) for node in node.expressions],
        ctx=python.Load(),
    )


# reference

@generate.register(tscl.Identifier)
def _(node, inline):
    return python.Name(
        id=node.value,
        ctx=python.Load(),
    )


# scoped

@generate.register(tscl.Function)
def _(node, inline):
    """
    Anonymous function node.

    Inline the function definition, and return the function identifier.
    """
    name = next(name_generator('lambda'))
    inline.append(python.FunctionDef(
        name=name,
        args=python.arguments(
            args=[python.arg(
                arg=param.value,
                annotation=None,
            ) for param in node.parameters.expressions],
            defaults=[],
            vararg=None,
            kwonlyargs=[],
            kw_defaults=[],
            kwarg=None,
        ),
        body=(
            [expr(generate(node, inline)) for node in node.expressions[:-1]]
            + [python.Return(value=generate(node.expressions[-1], inline))]
        ) if node.expressions else [python.Pass()],
        decorator_list=[],
        returns=None,
    ))
    return generate(
        tscl.Identifier(value=name),
        inline,
    )


@generate.register(tscl.Let)
def _(node, inline):
    """
    Let expression.

    Create an anonymous function, and return a call to the function identifier.
    """
    pass


# call

@generate.register(tscl.Call)
def _(node, inline):
    return python.Call(
        func=generate(node.expression, inline),
        args=[generate(node, inline) for node in node.expressions],
        keywords=[],
        starargs=None,
        kwargs=None,
    )


# helpers

def expr(node):
    return python.Expr(
        value=node,
    ) if not isinstance(node, python.FunctionDef) else node
