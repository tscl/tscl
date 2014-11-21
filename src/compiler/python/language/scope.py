"""
Bootstrap the tscl runtime environment with a root scope exposing the standard library.
"""
from collections import ChainMap

from .stdlib import core
from .stdlib import io

__all__ = [
    'scope',
]


scope = ChainMap(
    core.exports,
    io.exports,
    # ...
)
