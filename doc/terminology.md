
Terminology (proposals)
-----------------------

- "denote/refer": let's use this word for words/terms used in our
  conversations, so things that are in english (perhaps embellished
  with symbols) can denote things we like to talk aboute.

- "33s": (from 3Lisp/3Py/Cell): denotes any sort of semantically
  rationalized and reflective PL.

- "Cell": denotes the 33s that i'm currently working on, distinguished
  from 3py in that Cell has a different programming model.

- "function": i think we need to abandon this word completely, it's
  too overloaded. let's use the term "mathematical-function" to denote
  what closures designate -- and otherwise not use the word
  "function" at all.

- "procedure": denotes computational procedures, what i might
  loosely-speaking call a "function" in a programming language -- say,
  something defined in C or python.

- "structure" (STRUC): what i might otherwise call a
  configuration-of-bits (COB), denotes some specific internal
  arrangement of bits inside a computer. when talking about specific
  structures, enclose them in guillemots. note that this may not
  always be well-defined, but this is for human conversation only, so
  do a best-effort parse of what's inside. so for example, `«42»`
  denotes a structure that presumably has the bit pattern `..00101010`
  somewhere in it. the structural field is an assemblage of structures
  tied together by a web of effective relations.

- "realize/implement": denotes the relationship between something like
  bits and the structures

- we use the symbolic structure `a => b` to mean "(that which the term
  a denotes) denotes (that which the term b denotes)"

- "process": denotes particular concrete activity that happens inside
  a computer, in our context as a consequence of something provided to
  a 33s. this is what happens when a procedure executes (when a pair
  is reduced).

- "cusp": (confusingly unsaturated process) denotes an abstraction
  over processes, as is typically specified in a 33s by a method
  definition or lambda expression. in python, `def foo(x): ...` is
  associated with a cusp, and `foo(7)` is associated with a
  process; in 3Lisp, `(define foo (lambda simple [x] ...` is
  associated with a cusp, `(foo 7)` with a process.

- "interactive (console)": denotes a form of interaction with a 33s comprised of
  typing in text at a prompt and seeing results printed back on the
  console; the `read-normalise-print` of 3Lisp, or what you get when
  typing `python` at the terminal prompt.

- "input-string (console)" (IStr): denotes a sequence of characters entered into a
  prompt in console mode.

- "output-string (console)" (OStr): denotes a sequence of characters displayed on
  the console (not including prompt-like indicators) as a result of
  entering an input-string in console mode.

- "console-string" (CStr): denotes either an input-string or
  output-string. we can use backquotes to denote specific console
  strings, e.g. when typing the IStr `` `42` `` at the 3Lisp interactive
  prompt, the OStr `` `42` `` is printed. 

- "induces" (?): denotes the relationship between an input-string and
  a corresponding output-string at an interactive prompt. to
  symbolically denote this relationship use `IStr ~~> OStr` -- so, for
  example, `` `42` ~~> `42` ``.  note this is dependent upon the
  context/environment/state of the interactive interpreter, so that we
  may have `` `x` ~~> `3-Lisp run-time error: X is not bound` ``, yet later
  `` `x` ~~> `42` ``

- NOTE: if induction is dependent upon "mode" and that's relevant, we can
  indicate that within the arrow, e.g., `` `(+ 1 2)` ~i~> `3` ``

- "internalise": denotes a relationship between an input-string and the
  immediately consequent structure that results from that input-string.  so,
  `` `42` `` internalises to a structure (probably `«42»`) -- and we denote this
  symbolically by `` `42` ~< «42» ``. similarly, in 3Lisp, `` `(+ 1 2)` `` internalizes
  to a pair, `` `(+ 1 2)` ~< «(+ 1 2)» ``

- "externalise": denotes a relationship between a structure and an output-
   string, which we denote symbolically by `` STRUC >~ OStr ``, e.g.,
   `` «42» >~ `42` ``. NOTE: "internalise" and "externalise" do *NOT*, in general, make 
   up "induces"; so e.g., `` i ~~> o `` and `` i ~< s `` does not imply `` s >~ o ``.
   (e.g., in 3Lisp, the externalise of the structure that is the 
   normalisation of `s` in the current interactive environment is `o`).
   also, `` i ~< s >~ x `` does not necessarily mean `i` is the same as `x`.

- "normalise": denotes the 3Lisp operation between structures, which
  we can write `s1 -> s2` (`s1` normalises to `s2`)
