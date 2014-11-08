"""
Tokens and token matching
"""
import re

import lib

__all__ = [
    'next_token',
]

patterns = (
    ('WS', re.compile(r'^[ \t,]+')),
    ('NEWLINE', re.compile(r'^(\r\n|\r|\n)')),
    ('COMMENT', re.compile(r'^;[^\r|\n]*')),
    ('LPAREN', re.compile(r'^\(')),
    ('RPAREN', re.compile(r'^\)')),
    ('LBRACKET', re.compile(r'^\[')),
    ('RBRACKET', re.compile(r'^\]')),
    ('INTEGER', re.compile(r'^\-?\d+')),
    ('FLOAT', re.compile(r'^\-?\d+\.\d+')),  # float values -1 < n < 1 must be 0 prefixed, i.e.: -0.4
    # todo: STRING
    ('KEYWORD', re.compile(r'^(λ|fn|let|if|do)')),
    ('ATOM', re.compile(r'^:[^\s]+')),
    ('IDENTIFIER', re.compile(r'^[^\(\)\[\]\s\d][^\(\)\[\]\s]*')),  # no leading \d()[], no body ()[]
)


def next_token(string, token_patterns=patterns) -> "lib.Token | None":
    """
    Return the longest length token at the head of the input string, or None.
    """
    return max(next_candidates(string, token_patterns), key=lambda token: token.length)


def next_candidates(string, token_patterns=patterns) -> "(lib.Token,)":
    """
    Return a token generator for token patterns matching at the head of the input string.
    """
    for name, expression in token_patterns:
        match = re.match(expression, string)
        if match:
            value = match.group()
            yield lib.Token(name, value, len(value))
