
//---------------------
// syntactic shortcuts
//---------------------

syntactic_shortcut: up | down | assignment | constructor
//TAI: generator for ctor, etc

up: "↑" cell
down: "↓" cell_ref

assignment: cell_ref "=" cell
constructor: cell_def ":=" cell

