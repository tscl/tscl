"""
tscl io
"""

__all__ = [
    'exports',
]


def representation(value) -> "str":
    """
    Return the equivalent literal string representation of the value.
    """
    if isinstance(value, bool):
        return 'true' if value else 'false'
    if isinstance(value, (str, int, float)):
        return str(value)
    if isinstance(value, tuple):
        return '['+' '.join(map(representation, value))+']'  # todo: loop danger
    if isinstance(value, frozenset):
        return '{'+' '.join(map(representation, value))+'}'  # todo: loop danger
    raise NotImplemented('Unknown Representation')


exports = {
    'print': lambda *args: print(*map(representation, args))
}
