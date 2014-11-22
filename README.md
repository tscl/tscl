# tscl

A (lisp-ish) language for multiple environments.

## Interesting and Inspiring

* [Hy](https://github.com/hylang/hy)
* [wisp](https://github.com/Gozala/wisp)

## Introduction to tscl by Example

Print literal list, integer, float, and true & false boolean values:

`(print [-1 2.3 true false])` prints `[-1 2.3 true false]`

Write some equivalent expressions:

`(+ 1 2 3 4)` → `10`

`(apply + [1 2 3 4])` → `10`

`(apply + (map (λ [n] (+ 1 n)) (range 0 4)))` → `10`

`(reduce + [1 2 3 4])` → `10` and with an accumulator `(reduce + 1 [2 3 4])` → `10`

Lexical scope and closures:

```
(map 
 ;; a 10x multiplier
 ((λ [n] 
     (λ [i] (* n i))) 
   10)
 (range 1 11))
```

→ `[10 20 30 40 50 60 70 80 90 100]`

Let expressions:

```
(let [a 1
      b (+ a 1)
      c (* b 10)]
  [a b c])
```

→ `[1 2 20]`

## Literate Programming:

Source files may be written as plain tscl source, or as Markdown files with tscl source in fenced code blocks. In fact,
the README.md you're reading is a valid tscl source file.

```tscl
(print 42)
```

Running this file will print `42`.

The form above is evaluated when this file is interpreted because it:

* is not indented
* is fenced with tripple backticks
* includes the `tscl` language identifier

The form below does not meet these criteria and will not be evaluated:

    ```tscl
    (print 42)
    ```

----------

tscl was started at [Hack Nashville 6](http://hacknashville.com/).

!["Hack Nashville 6"](https://cloud.githubusercontent.com/assets/542163/5013839/9b44d120-6a56-11e4-8cd8-0a0ae1cbc475.png)
