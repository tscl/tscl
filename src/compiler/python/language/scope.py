"""
Bootstrap the tscl runtime environment with a root scope exposing the standard library.
"""
from collections import ChainMap

from .stdlib import placeholder

__all__ = [
    'scope',
]


scope = ChainMap(
    placeholder.exports,
    # ...
)
