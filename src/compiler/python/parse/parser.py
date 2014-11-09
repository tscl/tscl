"""
Parse tscl tokens into a parse tree (concrete syntax tree) representing tscl's formal grammar.

This is a multi-pass phase, consisting of:
- nodes(tokens): convert tokens into cst nodes with location data
- tree(nodes): convert nodes to a tree (nested list) data structure
- cst(tree): convert the un-checked tree into a grammatically correct CST
"""
import collections

import lib


def parse(tokens) -> "(lib.CSTNode)":
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
        line_start = cursor.line_end + (1 if (previous_token and previous_token.name == 'NEWLINE') else 0)
        line_end = cursor.line_end + (1 if (previous_token and previous_token.name == 'NEWLINE') else 0)  # not right
        col_start = 0 if (previous_token and previous_token.name == 'NEWLINE') else cursor.col_end
        col_end = col_start + token.length  # which means this is wrong, too

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
    Transform flat CST nodes into nested list tree structures.
    """
    stack = collections.deque()
    stack.append([])

    start_names = ('LPAREN', 'LBRACKET')
    end_names = ('RPAREN', 'RBRACKET')
    name_pairs = tuple(zip(start_names, end_names))

    for node in nodes:
        branch = stack[0]

        # start branch?
        if node.name in start_names:
            branch = [node]
            stack.appendleft(branch)
        # end branch? match parenthesis or brackets
        elif node.name in end_names:
            if (branch[0].name, node.name) not in name_pairs:
                raise Exception('Parse Error')
            # pop the current branch off the stack and append it to the top branch
            branch = stack.popleft()
            branch.append(node)
            stack[0].append(tuple(branch))
        # add node to the current branch
        else:
            branch.append(node)

    if len(stack) != 1:
        raise Exception("Parse Error")

    return tuple(stack[0])


def cst(tree):
    """
    Enforce the grammar and drop unnecessary nodes.
    """
    return tree
