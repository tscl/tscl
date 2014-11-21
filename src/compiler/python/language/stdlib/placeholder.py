"""
**STUB**

This is just a placeholder.
"""
import operator
from functools import reduce

from language.stdlib import objects

__all__ = [
    'exports',
]


exports = {
    # math
    '+': lambda *args, scope=None: reduce(operator.add, args),
    '-': lambda *args, scope=None: reduce(operator.sub, args),
    '*': lambda *args, scope=None: reduce(operator.mul, args),
    '/': lambda *args, scope=None: reduce(operator.truediv, args),

    # predicates
    'eq?': lambda *args, scope=None: objects.Boolean(all(map(lambda v: operator.eq(args[0], v), args))),

    # io
    'print': lambda *args, scope=None: print(*args),

    # data
    'bool': lambda *args, scope=None: objects.Boolean(*args),
    'int': lambda *args, scope=None: int(*args),
    'float': lambda *args, scope=None: float(*args),
    'set': lambda *args, scope=None: set(*args),
    'list': lambda *args, scope=None: objects.List(args),
    'range': lambda *args, scope=None: objects.List(range(*args)),

    # hof
    'map': lambda *args, scope=None: objects.List(map(*args)),
    'reduce': lambda *args, scope=None: reduce(*args),  # todo: make sure return value is the right type
}
