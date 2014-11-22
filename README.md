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

Let Expressions and Destructuring:

```
(let [a 0
      [a b c] (map inc (range a (+ a 3)))]
  [a b c])
```

→ `[1 2 3]`

Making decisions:

`(if true 1 0)` → `1`

`(if false 1 0)` → `0`

## Literate Programming

Source files may be written as plain tscl source, or as Markdown files with tscl source in fenced code blocks. In fact,
the README.md you're reading is a valid tscl source file.

```tscl
(print 42)
```

Running this file will print `42`.

The form above is evaluated when this file is interpreted because it:

* is not indented
* is fenced with triple backticks
* includes the `tscl` language identifier

The following illustrates the criteria above, but does not itself meet the criteria and will not be evaluated:

    ```tscl
    (print 42)
    ```
## No Names

You may have noticed that there are no named functions in the examples. This is because there are no named functions in
tscl; there are only anonymous closures.


----------

tscl was started at [Hack Nashville 6](http://hacknashville.com/).

!["Hack Nashville 6"](https://cloud.githubusercontent.com/assets/542163/5013839/9b44d120-6a56-11e4-8cd8-0a0ae1cbc475.png)
