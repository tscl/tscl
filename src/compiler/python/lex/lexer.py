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
    with open(path, 'r', encoding='utf-8') as source:
        yield from lexs(source.read())


def lexs(string) -> "(lib.Token,)":
    """
    Lex the given source string.
    """
    cursor = 0
    while cursor < len(string):
        token = lex.tokens.next_token(string[cursor:])
        cursor += token.length
        yield token
