

// the interpreter, when parsing a program file
// always produces a cop, which is in spirit `main`
// TAI: library files, modules, etc -- what's the right way
//   --> which is essentially a collection of named cells that other programs can use
//   --> another context you can merge-in; probably do objects first, then get there
interpreter: cop_body

// interactive mode: individual steps or ability to see cells
interactive: cop_step | cell


//---------------------
// kernel
//---------------------

cop: "!" cop_params "{" cop_body "}"
cop_params: "[" (cell_spec ",")* cell_spec? "]"
cop_body: (cop_step (";" | "\n"))* cop_step?
cop_step: cell_def | do | syntactic_shortcut | comment

do: do_call
do_call: do_op do_args
do_op: cell
do_args: "(" (cell ",")* cell? ")"

cell_spec: cell_name (":" cell_name )?
cell_def: "|" cell_spec "|" (">" constant)?
cell: cell_ref
cell_name: NAME
cell_ref: cell_name


//----------------------
// constants
//----------------------

constant: cop | literal

literal: STRING | INTEGER | REAL | BOOLEAN | NIL


//----------------------
// guts
//----------------------

comment: /#[^\n]*/

DIGIT: "0".."9"
LETTER: "a".."z" | "A".."Z"
ALPHA_WORD: LETTER+
WORD: ( "_" LETTER | "_" DIGIT | "__" | LETTER ) ( "_" | LETTER | DIGIT )*
NAME: WORD

INTEGER: ("+"|"-")? DIGIT+
DECIMAL: ("+"|"-")? ((DIGIT+ "." DIGIT*) | (DIGIT* "." DIGIT+))
REAL: DECIMAL
NUMBER: REAL | INTEGER
BOOLEAN: "$t" | "$f"
NIL: "$nil"

STRING_INNER: ("\\\""|/[^"]/)
ESCAPED_STRING: "\"" STRING_INNER* "\""

STRING: ESCAPED_STRING

//STRING_INNER_SQ: ("\\'"|/[^']/)
//ESCAPED_STRING_SQ: "'" STRING_INNER_SQ* "'"
//STRING: ESCAPED_STRING | ESCAPED_STRING_SQ

WHITESPACE: " " | "\n"
%ignore WHITESPACE
