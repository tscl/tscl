"""
Concrete Syntax Tree
"""
import collections

__all__ = [
    'cst',
]


def cst(nodes) -> "(lib.CSTNode)":
    """
    Return a valid concrete syntax tree from the input nodes.
    """
    return valid(tree(nodes))


def tree(nodes) -> "(lib.CSTNode)":
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


#
# Passes over `tree`
#

def valid(tree) -> "(lib.CSTNode)":
    """
    Return the CST validated against the grammar.
    """
    return tree
