
Terminology (proposals)
-----------------------

- "denote": let's use this word for words/terms used in our
  conversations, so things that are in english (perhaps embellished
  with symbols) can denote things we like to talk aboute.

- "33s": (from 3Lisp/3Py/Slot): denotes any sort of semantically
  rationalized and reflective PL.

- "Slot": denotes the 33s that i'm currently working on, distinguished
  from 3py in that Slot has a different programming model.

- "function": i think we need to abandon this word completely, it's
  too overloaded. let's use "ST-function" to denote "set-theoretic
  function" -- assuming, Brian, that this how you mean it in your
  diagram, what closures designate -- and otherwise not use the word
  "function" at all. for what i might loosely-speaking call a
  "function" in a programming language -- say, something defined in C
  or python -- let's use another term such as "method" or "procedure".

- "structure" (STRUC): what i might otherwise call a
  configuration-of-bits (COB), denotes some specific internal
  arrangement of bits inside a computer. when talking about specific
  structures, enclose them in guillemots. note that this may not
  always be well-defined, but this is for human conversation only, so
  do a best-effort parse of what's inside. so for example, `«42»`
  denotes a structure that presumably has the bit pattern `..00101010`
  somewhere in it.

- "referent": denotes something that is designated (below) by a
  structure

- "designation": denotes a technical relationship between structures
  and referents. we write structure `=>` referent.

- "process": denotes a specific sequence of steps that happens inside
  a computer, in our context as a consequence of something provided to
  a 33s. this is what happens when a method executes (when a pair is
  reduced).

- "behavior": denotes an abstraction over processes, as is typically
  specified in a 33s by a method definition or lambda expression. in
  python, `def foo(x): ...` is associated with a behavior, and
  `foo(7)` is associated with a process; in 3Lisp, `(define foo
  (lambda simple [x] ...` is associated with a behavior, `(foo 7)`
  with a process.

- "interactive": denotes a form of interaction with a 33s comprised of
  typing in text at a prompt and seeing results printed back on the
  console; the `read-normalise-print` of 3Lisp, or what you get when
  typing `python` at the terminal prompt.

- "input-string" (IStr): denotes a sequence of characters entered into a
  prompt in interactive mode.

- "output-string" (OStr): denotes a sequence of characters displayed on
  the console (not including prompt-like indicators) as a result of
  entering an input-string in interactive mode.

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

- "parse": denotes a relationship between an input-string and the
  immediately consequent structure induced by that input-string.  so,
  `` `42` `` parses to a structure (probably `«42»`) -- and we denote this
  symbolically by `` `42` ~< «42» ``. similarly, in 3Lisp, `` `(+ 1 2)` `` parses
  to a pair; i can see writing either `` `(+ 1 2)` ~< «(+ 1 2)» ``, OR 
  `` `(+ 1 2)` ~< «'(+ 1 2)» `` -- TBD -- but regardless of how the parsed
  structure is written, it should be understood to be a pair.

- "repr": denotes a relationship between a structure and an output
   string, which we denote symbolically by `` STRUC >~ OStr ``, e.g.,
   `` «42» >~ `42` ``. NOTE: "parse" and "repr" do *NOT*, in general, make 
   up "induces"; so e.g., `` i ~~> o `` and `` i ~< s `` does not imply `` s >~ o ``.
   (e.g., in 3Lisp, the repr of the structure that is the 
   normalisation of `s` in the current interactive environment is `o`).

- "normalise": denotes the 3Lisp operation between structures. i want
  to use `=>` for designate, though we could use that here and
  something else? `=n=>`? suggestions?
