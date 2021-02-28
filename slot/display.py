
from . import model as M


def _displayType(x):
    return (x.human.displayType or x.human.name or "??") if (x and x.human) else "??"

def displayStructure(x):
    t = type(x).__name__
    if isinstance(x, M.Slot):
        d = _displayType(x.slotType)
    elif isinstance(x, M.MetaSlot):
        d = _displayType(x.slotType)
        if x.concrete:
            d += "(concrete)"
        elif x.instanced:
            d += "(instanced)"
    elif isinstance(x, M.Slop):
        d = "..." # TBD
    elif isinstance(x, M.Slex):
        d = "..."  # TBD
    elif callable(x):
        d = impl.__name__
    elif hasattr(x, 'json'):
        d = x.json()
        d = str(d)
        if len(d) > 32:
            d = d[:28] + "...}"
    else:
        d = repr(x)
    return "<< {} : {} >>".format(t, d)

_designationTypeLookup = {
    "NoneType" : "Nil",
    "Nil" : "Nil",
    "Boolean" : "Truth Value",
    "bool" : "Truth Value",
    "Integer" : "Number",
    "int" : "Number",
    "Real" : "Real Number",
    "float" : "Real Number",
    "str" : "Word",
    "String" : "Word",
    "Slop" : "Behavior",
    "Slex" : "Process",
}

def displayDesignation(x):
    t = None
    if isinstance(x, M.Slot):
        if x.slotType:
            t = x.slotType.human.name
        if (not t) or (t == 'Generic'):
            t = type(x.data).__name__
        if hasattr(x.data, 'fsType'): # is it a model object?
            d = "..."
        elif (x.data == None):
            d = 'Nil'
        else:
            d = str(x.data)
    if (not t) or (t not in _designationTypeLookup):
        #print(t, x)
        return "{Undefined designation}"
    return "{{{}:{}}}".format(_designationTypeLookup[t], d)
