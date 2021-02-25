
Detail questions/issues
-----------------

- pursuant to issue (1), consider the following 3Lisp session:

```
0 > (set x 'abc)
0 = 'OK
0 > (set y 'abc)
0 = 'OK
0 > (= x y)
0 = $T
```

to me as a CITW programmer, this is a blatant re-purposing of atoms as
strings -- for example, as used in the 3Lisp reflective processor
"(procedure-type proc!)" -- doing string-compares on things called
atoms. it seems to me that for semantic clarity, there should be a
distinction between "character sequences that can be compared to
control program flow" and "things used to look up environment
bindings". 


- i was glad to see that READ/PRINT/INPUT/OUPUT are not categorizd as
  3Lisp-kernel. they are required for the 3lisp-interactive UI
  (read-normalise-print), but not beyond that

- in my previous mail ("towards 3-python"), i think i tried to bite
  off too many things at once. the goal is to pick at some of the
  issues above, and also give us a context for speaking *both* about
  designations and corresponding structures that designate -- not to
  try to re-frame how we should go about doing semantically-laden
  programming.

  so, let me try to re-phrase part of it, but stay wholly in the
  context of 3Lisp. the proposal aims to disentangle parsing, structures
  and normalisation, and also avoid confusion/conflation between
  input-strings, output-strings, and structures.

  so consider an alternate UI/HCI, call it for now
  "jims-weird-3Lisp-UI", as opposed to "read-normalise-print". this
  has no effect on the 3Lisp reflective processor (anything kernel),
  it just changes how we interact with it. maybe this is something
  like a debugging version -- not a serious proposal for a new
  end-user version. but it's critical that this has no proposed change
  to the 3Lisp kernel, just an alternative way of interacting with it.

  so, jims-weird-3Lisp-UI has 4 distinct "modes": "i" for interactive,
  which is the default and does the same as read-normalise-print; "s"
  for structural; "d" for designating; and "n" for
  normalising. easiest to describe via a sample session:

```
0 i> 3
 3
0 i> (+ 1 2)
 3
0 i> [1 2 3]
 [1 2 3]
0 i> x
3-Lisp run-time error: X is not bound
0 i> .s
 [[ Now in strucural mode ]]
0 s> 3
 {NUMERAL:3}
0 s> (+ 1 2)
 {PAIR:...}
0 s> [1 2 3]
 {RAIL:...}
0 s> x
 {ATOM:x}
0 s> .d
 [[ Now in designation mode ]]
0 d> 3
 {NUMBER:3}
0 d> (+ 1 2)
 Error: designation is undefined
0 d> [1 2 3]
 {SEQUENCE:[1 2 3]}
0 d> x
 Error: designation is undefined
0 d> .n
 [[ Now in normalisation mode ]]
0 n> 3
 {NUMBER:3}
0 n> (+ 1 2)
 {NUMBER:3}
0 n> [1 2 3]
 {SEQUENCE:[1 2 3]}
0 n> x
 Error: X is not bound
```

some notes:
- i switched to the 3Lisp "notational escape" `{ }` instead of `< >`
- the output for all non-"i" modes is intentionally fully-escaped and
  weird; want to be clear that those are OStr, avoid DSQ issues
- normalisation only happens in "i"-mode and "n"-mode, never in "d"-mode and "s"-mode
- "d"-mode and "s"-mode work with directly-parsed structures; you can
  sort of think of it as having an implicit quote added to anything you type

i propose this as a way to tease apart things are tied together
implicitly in the read-normalise-print loop. we can also sketch the
implementation of this, which i think is instructive:

- first, need to tease apart the `read` (used in `prompt&read` in the
  reflective processor) and `print` (used in `prompt&reply`) methods.
  a little "mystery" is ok -- but i think it's hiding too much there... :)

```
; phi [ STREAMS ] -> STRUCTURES
(define READ (lambda simple [stream]
             (parse (read-balanced-string stream))))

; phi [ STRINGS ] -> STRUCTURES
(define PARSE (lambda simple [string]) (mystery))

; phi [ STREAMS ] -> STRINGS
(define READ-BALANCED-STRING (lambda simple [stream]) (mystery))

; phi [ STRINGS x STREAMS ] -> ATOMS
(define PRINT (lambda simple [string stream] (print-string string stream)))

; phi [ STRUCTURES ] -> STRINGS
(define REPR (lambda simple [struc] (mystery)))

; and then PROMPT&REPLY should use `(print (repr answer) stream)`
; instead of `(print answer stream)` -- and print-string can be 
; called `print`
```

- now, we can sketch out the alternative UI impl:

```
(set JIMS-UI-MODE 'i)

(define JIMS-WEIRD-3LISP-UI (lambda simple [env stream]
    (let [ [resp! (prompt&read-string stream)]
           [cont! (lambda simple [result] (block (prompt&write-string (repr result)) (jims-weird-3lisp-ui env stream)))]
           [jcont! (lambda simple [result] (block (prompt&write-string (jims-repr result)) (jims-weird-3lisp-ui env stream)))] ]
        (if (jims-command? resp!)
            (block (set jims-ui-mode (jims-get-mode resp!))
                   (prompt&write-string "'OK")
                   (jims-weird-3lisp-ui env stream))
            (selectq jims-ui-mode
              [i (normalise (parse resp!) env cont!)]
              [s (jcont! ↑(parse resp!))]
              [d (jcont! (parse resp!))]
              [n (normalise (parse resp!) env jcont!)])))))

(define JIMS-REPR (lambda simple [struc]
  (string-concat "{"
                 (repr (type struc))
                 ":"
                 (if (normal struc) (repr struc) "...")
                 "}")))
```

it may be worth reviewing together at some point whether what i have
here makes sense to a seasoned 3Lisp-er... :)

- but main question is -- does this still seem like it has the same
  worry as the proposal from the last email? if so i really want to
  worry that out until we have an understanding!
