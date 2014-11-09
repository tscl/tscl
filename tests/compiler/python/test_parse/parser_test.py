import nose.tools

from lex import lexer
from parse import parser


def parse_test():
    """
    Parse tokens.
    """
    source = """
    ;;;; This is some test source code

    (let [this source-code]   ; open
        ((lex) into) tokens)  ; close

    (let [this source-code]
        :lex-into tokens too!)
    """
    lines = [line+'\n' for line in source.split('\n')]
    cst = parser.parse(lexer.lexs(source))

    def test_branch(branch):
        """A branch must start and end with the correct closing tokens."""
        assert 2 <= len(branch)

        start_names = ('LPAREN', 'LBRACKET')
        end_names = ('RPAREN', 'RBRACKET')
        start_name, end_name = branch[0].name, branch[-1:][0].name

        assert start_name in start_names
        assert end_name in end_names
        assert (start_name, end_name) in zip(start_names, end_names)

    def test_leaf(leaf):
        """A leaf must contain the correct location information."""
        # position start and end
        assert leaf.value == source[leaf.location.pos_start:leaf.location.pos_end]

        # single line column start and end
        if leaf.location.line_start == leaf.location.line_end:
            print((leaf, lines[leaf.location.line_start][leaf.location.col_start:leaf.location.col_end]))
            assert leaf.value == lines[leaf.location.line_start][leaf.location.col_start:leaf.location.col_end]

        # single line column start and end
        if leaf.location.line_start != leaf.location.line_end:
            raise NotImplementedError('Multi-line nodes are not yet supported')

    def test_tree(tree):
        """Test each branch and leaf in the tree."""
        for node in tree:
            if isinstance(node, tuple):
                test_branch(node)
                test_tree(node)
            else:
                test_leaf(node)

    test_tree(cst)


@nose.tools.raises(Exception)
def parse_unbalanced_paren_test():
    """
    Fail to parse tokens due to unbalanced parentheses.
    """
    source = """
    (+ 1 (* 2 3)
    """
    parser.parse(lexer.lexs(source))

@nose.tools.raises(Exception)
def parse_unbalanced_bracket_test():
    """
    Fail to parse tokens due to unbalanced square brackets.
    """
    source = """
    (let [1 (* 2 3)))
    """
    parser.parse(lexer.lexs(source))
