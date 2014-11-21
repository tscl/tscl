"""
**STUB**

This is just a placeholder.
"""
import operator
from functools import reduce

__all__ = [
    'exports',
]


exports = {
    # math
    '+': lambda *args: reduce(operator.add, args[1:]),
    '-': lambda *args: reduce(operator.sub, args[1:]),
    '*': lambda *args: reduce(operator.mul, args[1:]),
    '/': lambda *args: reduce(operator.truediv, args[1:]),

    # io
    'print': lambda *args: print(*args[1:]),

    # data
    'int': lambda *args: int(*args[1:]),
    'float': lambda *args: float(*args[1:]),
    'list': lambda *args: list(*args[1:]),
    'set': lambda *args: set(*args[1:]),
    'range': lambda *args: range(*args[1:]),
}
