from lex import lexer
from parse import parser
from abstract import tree
from generate import python_ast


def compiles(string):
    generated_ast = python_ast.generate(tree.ast(parser.parse(lexer.lexs(string))))
    return compile(generated_ast, '<test>', 'exec')


def eval_test():
    eval(compiles('1'))
    eval(compiles('1.0'))
    eval(compiles('[1 2 3]'))
    eval(compiles('(print 1 2 3)'))
    eval(compiles('((fn [a] (print a)) 1)'))
    eval(compiles('((fn [a b] (print a) (print b) (print a b)) 1 2)'))
    eval(compiles('''
    (print
      ((fn [f bar baz]
          (f bar baz)
          100)
        (fn [a b] (print (list (range a b))))
        1
        10))
    '''))
