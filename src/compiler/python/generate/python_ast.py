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
    inline_children = []
    children = [expr(generate(node, inline_children)) for node in node.expressions]
    return python.fix_missing_locations(
        python.Module(
            body=[
                # import the root scope
                python.ImportFrom(module='language.scope', names=[python.alias(name='scope', asname=None)], level=0),
                # the program, with necessary statements in-lined before they are referenced in expressions
            ] + inline_children + children,
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
    return python.Call(
        func=python.Subscript(
            value=python.Name(id='scope', ctx=python.Load()),
            slice=python.Index(value=python.Str(s='list')),
            ctx=python.Load(),
        ),
        args=[generate(node, inline) for node in node.expressions],
        keywords=[], starargs=None, kwargs=None,
    )


# reference

@generate.register(tscl.Identifier)
def _(node, inline):
    return python.Subscript(
        value=python.Name(id='scope', ctx=python.Load()),
        slice=python.Index(
            value=python.Str(s=node.value),
        ),
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
    inline_children = []
    children = [expr(generate(node, inline_children)) for node in node.expressions]
    inline.append(python.FunctionDef(
        name=name,
        args=python.arguments(
            args=[
                python.arg(arg=param.value, annotation=None) for param in node.parameters.expressions
            ],
            defaults=[],
            vararg=None,
            kwonlyargs=[
                python.arg(arg='scope', annotation=None),
            ],
            kw_defaults=[
                python.Name(id='scope', ctx=python.Load()),
            ],
            kwarg=None,
        ),
        body=(
            [
                # create the function scope, initialized with the function locals
                python.Assign(
                    targets=[python.Name(id='scope', ctx=python.Store())],
                    value=python.Call(
                        func=python.Attribute(
                            value=python.Name(id='scope', ctx=python.Load()),
                            attr='new_child', ctx=python.Load()
                        ),
                        args=[python.Call(
                            func=python.Name(id='locals', ctx=python.Load()), args=[],
                            keywords=[], starargs=None, kwargs=None
                        )],
                        keywords=[], starargs=None, kwargs=None,
                    )
                )
                # function body with in-lined statements, returning the last expression
            ] + inline_children + children[:-1] + [python.Return(value=children[-1].value)]
            # or pass if no body
        ) if node.expressions else [python.Pass()],
        decorator_list=[],
        returns=None,
    ))
    return python.Name(
        id=name,
        ctx=python.Load(),
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
    """
    Call a function, passing the current scope.
    """
    return python.Call(
        func=generate(node.expression, inline),
        args=[
            generate(node, inline) for node in node.expressions
        ],
        keywords=[],
        starargs=None,
        kwargs=None,
    )


# helpers

def expr(node):
    return python.Expr(
        value=node,
    ) if not isinstance(node, python.FunctionDef) else node
