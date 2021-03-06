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
    children = [wrap(generate(node, inline_children)) for node in node.expressions]
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

@generate.register(tscl.Boolean)
def _(node, inline):
    return python.NameConstant(value=True) if node.value == 'true' else python.NameConstant(value=False)

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
    return python.Tuple(
        elts=[generate(node, inline) for node in node.expressions],
        ctx=python.Load(),
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
def _(node, inline, bindings=()):
    """
    Anonymous function node.

    Inline the function definition, and return the function identifier.
    """
    name = next(name_generator('lambda'))
    inline_children = []

    # bindings in local scope
    binding_assignments = [
        python.Assign(
            targets=[
                python.Tuple(
                    elts=[
                        python.Subscript(
                            value=python.Name(id='scope', ctx=python.Load()),
                            slice=python.Index(
                                value=python.Str(s=identifier.value),
                            ),
                            ctx=python.Store(),
                        ) for identifier in (identifier.expressions if (isinstance(identifier, tscl.List)) else [identifier])
                    ],
                    ctx=python.Store(),
                )
            ],
            value=(
                # expression: assume iterable if identifier expects destructuring
                generate(expression, inline_children) if (
                    isinstance(identifier, (
                        tscl.List,
                    )) and isinstance(expression, (
                        tscl.Let,
                        tscl.Call,
                        tscl.Identifier,
                    ))
                ) else

                # reference: may or may not evaluate to an iterable
                generate(expression, inline_children) if isinstance(expression, (
                    tscl.Identifier,
                )) else

                # list: wrap nested expressions in tuple if identifier expects destructuring
                python.Tuple(
                    elts=[generate(expression, inline_children) for expression in expression.expressions],
                    ctx=python.Load(),
                ) if (isinstance(identifier, tscl.List) and isinstance(expression, tscl.List)) else

                # value or expression: wrap in tuple
                python.Tuple(
                    elts=[generate(expression, inline_children)],
                    ctx=python.Load(),
                )
            )
        )
        for identifier, expression in zip(bindings[::2], bindings[1::2])
    ]
    children = [wrap(generate(node, inline_children)) for node in node.expressions]
    inline.append(python.FunctionDef(
        name=name,
        args=python.arguments(
            args=[
                python.arg(arg=param.value, annotation=None) for param in node.parameters.expressions
            ],
            defaults=[],
            vararg=None,
            # capture current scope and create a new child scope to pass into the function
            kwonlyargs=[
                python.arg(arg='scope', annotation=None),
            ],
            kw_defaults=[
                python.Call(
                    func=python.Attribute(
                        value=python.Name(
                            id='scope', ctx=python.Load()
                        ),
                        attr='new_child', ctx=python.Load(),
                    ),
                    args=[], keywords=[], starargs=None, kwargs=None,
                ),
            ],
            kwarg=None,
        ),
        body=(
            [
                # update scope with function locals
                wrap(python.Call(
                    func=python.Attribute(
                        value=python.Name(id='scope', ctx=python.Load()),
                        attr='update', ctx=python.Load(),
                    ),
                    args=[
                        python.Call(
                            func=python.Name(id='locals', ctx=python.Load()),
                            args=[], keywords=[], starargs=None, kwargs=None)
                    ],
                    keywords=[], starargs=None, kwargs=None
                ))
                # function body with in-lined statements and bindings (let ...), returning the last expression
            ] + inline_children + binding_assignments + children[:-1] + [python.Return(value=children[-1].value)]
            # or pass if no body
        ) if node.expressions else [python.Pass()],
        decorator_list=[],
        returns=None,
    ))
    # the function itself will be inlined in a parent scope; return an identifier for the function
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
    name = generate(
        tscl.Function(
            parameters=tscl.List(expressions=()),
            expressions=node.expressions,
        ),
        inline,
        node.bindings.expressions,
    )
    return python.Call(
        func=name, args=[], keywords=[], starargs=None, kwargs=None,
    )


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


# flow

@generate.register(tscl.If)
def _(node, inline):
    return python.IfExp(
        test=generate(node.expression, inline),
        body=generate(node.then_expression, inline),
        orelse=generate(node.else_expression, inline),
    )


# helpers

def wrap(node):
    return python.Expr(
        value=node,
    ) if not isinstance(node, python.FunctionDef) else node
