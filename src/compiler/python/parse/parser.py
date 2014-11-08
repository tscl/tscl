"""
Parse tscl tokens into a parse tree (concrete syntax tree) representing tscl's formal grammar.

This is a multi-pass phase, consisting of:
- nodes(tokens): convert tokens into cst nodes with location data
- tree(nodes): convert nodes to a tree (nested list) data structure
- cst(tree): convert the un-checked tree into a grammatically correct CST
"""
import collections

import lib


def parse(tokens) -> "[lib.CSTNode,]":
    """
    Transform tokens into an iterable of concrete syntax trees.
    """
    return cst(tree(nodes(tokens)))


def nodes(tokens) -> "(lib.CSTNode,)":
    """
    Generate flat CST nodes with location information from tokens.
    """
    cursor = lib.Location(0, 0, 0, 0, 0, 0)
    previous_token = None

    for token in tokens:
        pos_start = cursor.pos_end
        pos_end = pos_start + token.length
        line_start = cursor.line_end + 1 if (previous_token and previous_token.name == 'NEWLINE') else 0
        col_start = cursor.col_end
        line_end = line_start  # this is wrong
        col_end = col_start + token.length  # which means this is, too

        cursor = lib.Location(pos_start, pos_end, line_start, col_start, line_end, col_end)
        node = lib.CSTNode(
            name=token.name,
            value=token.value,
            location=cursor,
        )

        previous_token = token
        yield node


def tree(nodes) -> "[lib.CSTNode]":
    """
    Illustration:
        parse("(+ 6 (- 5 4) 3)\n(* 2 1)") -> [
            ['(', '+', '6', ['(', '-', '5', '4', ')'], '3', ')'],
            ['(', '*', '2', '1', ')'],
        ]
    """
    stack = collections.deque()
    stack.append([])

    for node in nodes:
        branch = stack[0]

        # manage the branch stack
        if node.name in ('LPAREN', 'LBRACKET'):
            # push a new branch on the stack
            branch = []
            stack.appendleft(branch)
        elif node.name in ('RPAREN', 'RBRACKET'):
            # pop the current branch off the stack and append it to the top branch
            branch = stack.popleft()
            stack[0].append(branch)

        # add node to the current branch
        branch.append(node)

    if len(stack) != 1:
        raise Exception("Parse Error")

    return stack[0]


def cst(tree):
    """
    Validate
    """
    return tree
