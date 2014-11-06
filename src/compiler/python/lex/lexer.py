"""
Generate tokens from tscl source code.
"""
import lex.tokens

__all__ = [
    'lexf',
    'lexs',
]


def lexf(path) -> "(lib.Token,)":
    """
    Lex a source code file at the given path.
    """
    with open(path, 'r') as source:
        for line in source:
            yield from lexs(line)


def lexs(string) -> "(lib.Token,)":
    """
    Lex the given string.
    """
    column = 0
    while column < len(string):
        token = lex.tokens.next_token(string[column:])
        yield token
        column += token.length
