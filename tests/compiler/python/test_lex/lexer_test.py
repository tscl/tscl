import mock

from lex import lexer


def lexf_test():
    """
    Lex a file.
    """
    with mock.patch('lex.lexer.open', mock.mock_open(read_data='(λ)'), create=True) as mock_open:
        tokens = list(lexer.lexf('foo.tscl'))

    mock_open.assert_called_once_with('foo.tscl', 'r', encoding='utf-8')
    assert 3 == len(tokens)


def lexs_sanity_test():
    """
    The simplest cases of token names and sample token values which must match.
    """
    expectations = {
        'WS': (
            ' \t,',
        ),
        'NEWLINE': (
            '\n',
            '\r',
            '\r\n',
        ),
        'COMMENT': (
            '; foo',
        ),
        'LPAREN': '(',
        'RPAREN': ')',
        'LBRACKET': '[',
        'RBRACKET': ']',

        'INTEGER': (
            '123',
            '-23',
        ),
        'FLOAT': (
            '0.1',
            '-0.23',
        ),
        'KEYWORD': (
            'λ',
            'fn',
            'let',
            'if',
            'do',
        ),
        'ATOM': (
            ':f(o)o[].',
        ),
        'IDENTIFIER': (
            '-foo-42.bar',
        ),
    }
    for name, values in expectations.items():
        for value in values:
            tokens = list(lexer.lexs(value))
            assert 1 == len(tokens)
            token = tokens[0]
            assert len(value) == token.length
            try:
                assert name == token.name
            except AssertionError:
                print(name, token.name)
                raise
