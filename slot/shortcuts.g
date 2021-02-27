
//---------------------
// syntactic shortcuts
//---------------------

syntactic_slex_shortcut: assignment | constructor
syntactic_slot_shortcut: constant


//---------------------
// slex shortcuts
//---------------------

assignment: slot_ref "=" slot
constructor: slot_def ":=" slot


//---------------------
// slot shortcuts
//---------------------

constant: literal

literal: STRING | INTEGER | REAL | BOOLEAN | NONE

INTEGER: ("+"|"-")? DIGIT+
DECIMAL: ("+"|"-")? ((DIGIT+ "." DIGIT*) | (DIGIT* "." DIGIT+))
REAL: DECIMAL
NUMBER: REAL | INTEGER
BOOLEAN: "True" | "False"
NONE: "None"

STRING_INNER: ("\\\""|/[^"]/)
ESCAPED_STRING: "\"" STRING_INNER* "\""

STRING: ESCAPED_STRING

//STRING_INNER_SQ: ("\\'"|/[^']/)
//ESCAPED_STRING_SQ: "'" STRING_INNER_SQ* "'"
//STRING: ESCAPED_STRING | ESCAPED_STRING_SQ

