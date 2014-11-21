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

    # io
    'print': lambda *args, scope=None: print(*args),

    # data
    'int': lambda *args, scope=None: int(*args),
    'float': lambda *args, scope=None: float(*args),
    'set': lambda *args, scope=None: set(*args),
    'list': lambda *args, scope=None: objects.List(args),
    'range': lambda *args, scope=None: objects.List(range(*args)),
}
