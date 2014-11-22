"""
tscl core
"""
import operator
from functools import reduce

__all__ = [
    'exports',
]


exports = {
    # math
    '+': lambda *args, scope=None: reduce(operator.add, args),
    '-': lambda *args, scope=None: reduce(operator.sub, args),
    '*': lambda *args, scope=None: reduce(operator.mul, args),
    '/': lambda *args, scope=None: reduce(operator.truediv, args),
    'inc': lambda arg, scope=None: arg + 1,

    # predicates
    'eq?': lambda *args, scope=None: bool(all(map(lambda v: operator.eq(args[0], v), args))),

    # data
    'bool': lambda *args, scope=None: bool(*args),
    'int': lambda *args, scope=None: int(*args),
    'float': lambda *args, scope=None: float(*args),
    'set': lambda *args, scope=None: set(*args),
    'list': lambda *args, scope=None: tuple(args),
    'range': lambda *args, scope=None: tuple(range(*args)),

    # hof
    'apply': lambda f, args, scope=None: f(*args),
    'map': lambda f, args, scope=None: tuple(map(f, args)),
    'fold': lambda f, *args, scope=None: reduce(f, *reversed(args)),
}
