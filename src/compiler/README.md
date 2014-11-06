# Compiler

The tscl [compiler](http://en.wikipedia.org/wiki/Compiler#Structure_of_a_compiler) pipeline: 

`(generate (optimize (parse (lex (preprocess source-file)))))`

The tscl compiler is, conceptually, "a collection of modular and reusable" ([llvm.org](http://llvm.org/)) pieces of 
software, which may be composed to build an end-to-end pipeline, or may be used independently for any other purpose.

## Front End

`(preprocess source-file) -> source-code`

`(lex source-code) -> tokens`

`(parse tokens) -> cst`

## Middle End

`(optimize cst) -> ast`

## Back End

`(generate ast) -> target-code`

The tscl compiler is planned to support multiple targets
* Python AST
* JavaScript, [example](http://pyjs.org/Translator.html)
* LLVM IR
