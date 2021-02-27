

// the interpreter, when parsing a program file
// always produces a slop, which is in spirit `main`
// TAI: library files, modules, etc -- what's the right way
//   --> which is essentially a collection of named slots that other programs can use
//   --> another context you can merge-in; probably do objects first, then get there
interpreter: slop_body

// interactive mode
interactive: slop_step | slop | slot_ref | syntactic_slot_shortcut

//---------------------
// kernel defs
//---------------------


slop: "!" slop_params "{" slop_body "}"
slop_params: "[" (slot_spec ",")* slot_spec? "]"
slop_body: (slop_step ";")* slop_step?
slop_step: slex | slot_def | syntactic_slex_shortcut

slex: slex_call
slex_call: slex_op slex_args
slex_op: slot
slex_args: "(" (slot ",")* slot? ")"

slot_spec: slot_name (":" slot_name)?
slot_def: "|" slot_spec "|"
slot: slot_ref | slop_ref | slex_ref | syntactic_slot_shortcut
slot_name: NAME

slop_ref: slop
slex_ref: slex
slot_ref: slot_name


//----------------------
// TAI
//----------------------

//up: ("↑" | "UP") expr
//down: ("↓" | "DOWN") expr


//----------------------
// guts
//----------------------

DIGIT: "0".."9"
LETTER: "a".."z" | "A".."Z"
ALPHA_WORD: LETTER+
WORD: ( "_" LETTER | "_" DIGIT | "__" | LETTER ) ( "_" | LETTER | DIGIT )*
NAME: WORD

WHITESPACE: " "
%ignore WHITESPACE
