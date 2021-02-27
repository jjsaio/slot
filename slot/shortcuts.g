
//---------------------
// syntactic shortcuts
//---------------------

syntactic_shortcut: assignment | constructor

assignment: slot_ref "=" slot
constructor: slot_def ":=" slot
