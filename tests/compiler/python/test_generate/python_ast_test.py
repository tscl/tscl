from lex import lexer
from parse import parser
from abstract import tree
from generate import python_ast


def compiles(string):
    return compile(python_ast.generate(tree.ast(parser.parse(lexer.lexs(string)))), '<test>', 'exec')


def eval_test():
    eval(compiles('1'))
    eval(compiles('1.0'))
    eval(compiles('[1 2 3]'))
