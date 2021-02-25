
start: structure
// start: cli

cli: command

command: command_key structure?

command_key: NAME

structure: slot_def | slex | slop | slot

slot_def: "|" slot_spec "|" ("=" slot)?
//slot_def: "|" (atom ",")* atom? "|" value?

slot_spec: slot_name (":" slot_ref)?

slex: slex_call | syntactic_shortcut
slex_call: slex_op slex_args
slex_op: slot
slex_args: "(" (slot ",")* slot? ")"

slot: slot_ref | constant | slop

//slop: "!" "[" (slot_spec ",")* slot_spec? "]" ("<" (slot_spec ",")* slot_spec ">")? "{" (op ";")* op? "}"
slop: "!" slop_params slop_locals? slop_steps
slop_params: "[" (slot_spec ",")* slot_spec? "]"
slop_locals: "|" (slot_spec ",")* slot_spec? "|"
slop_steps: "{" (slex ";")* slex? "}"

slot_ref: NAME
slot_name: NAME

syntactic_shortcut: assignment
assignment: slot "=" slot

//up: ("↑" | "UP") expr
//down: ("↓" | "DOWN") expr

constant: literal 

literal: STRING | INTEGER | REAL | BOOLEAN | NONE

DIGIT: "0".."9"
LETTER: "a".."z" | "A".."Z"
ALPHA_WORD: LETTER+
WORD: ( "_" LETTER | "_" DIGIT | "__" | LETTER ) ( "_" | LETTER | DIGIT )*
NAME: WORD

INTEGER: ("+"|"-")? DIGIT+
DECIMAL: ("+"|"-")? ((DIGIT+ "." DIGIT*) | (DIGIT* "." DIGIT+))
REAL: DECIMAL
NUMBER: REAL | INTEGER
BOOLEAN: "True" | "False"
NONE: "None"

STRING_INNER: ("\\\""|/[^"]/)
ESCAPED_STRING: "\"" STRING_INNER* "\""

STRING: ESCAPED_STRING

WHITESPACE: " "
%ignore WHITESPACE
