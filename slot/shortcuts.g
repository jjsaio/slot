
//---------------------
// syntactic shortcuts
//---------------------

syntactic_shortcut: up | down | assignment | constructor
//TAI: generator for ctor, etc

up: "↑" slot
down: "↓" slot_ref

assignment: slot_ref "=" slot
constructor: slot_def ":=" slot

