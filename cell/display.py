
from . import model as M


def _displayType(x):
    return (x.human.displayType or x.human.name or "??") if (x and x.human) else "??"

def displayStructure(x):
    t = type(x).__name__
    if isinstance(x, M.Cell):
        d = _displayType(x.cellType)
    elif isinstance(x, M.MetaCell):
        if x.concrete:
            d = "C"
        else:
            d = "I"
        d = "{}[{}]".format(d, _displayType(x.cellType))
    elif isinstance(x, M.Cop) or isinstance(x, M.MetaCop):
        d = "..." # TBD
    elif isinstance(x, M.Do):
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

def debugString_Do(x):
    return "Do[{}({})]".format(debugString(x.op.op.human),
                                 ", ".join([ debugString(y.human) for y in x.args ]))

def debugString_MetaDo(x):
    return "MetaDo[{}({})]".format(debugString(x.op.human),
                                     ", ".join([ debugString(y.human) for y in x.args ]))

def debugString_Human(x):
    return x.name

def debugString_MetaCell(x):
    return "MetaCell[{}:{}:{}]".format("C" if x.concrete else "I",
                                       debugString(x.human),
                                       debugString(x.cellType.human))

def debugString_MetaCop(x):
    return "MetaCop[{}![{}]|{}|<{}>{{{}}}@{:x}]".format(debugString(x.human),
                                                         ", ".join([ debugString(y.human) for y in x.params]),
                                                         ", ".join([ debugString(y.human) for y in x.locals]),
                                                         ", ".join([ debugString(y.human) for y in x.captured]),
                                                         len(x.steps),
                                                         id(x) & 0xffff)

def debugString_Cop(x):
    return "Cop<{}>[{}![{}]|{}|<{}>{{{}}}@{:x}]".format(", ".join([ debugString(y.human) for y in x.captured]),
                                                         debugString(x.op.human),
                                                         ", ".join([ debugString(y.human) for y in x.op.params]),
                                                         ", ".join([ debugString(y.human) for y in x.op.locals]),
                                                         ", ".join([ debugString(y.human) for y in x.op.captured]),
                                                         len(x.op.steps),
                                                         id(x) & 0xffff)

# TBD...

def debugString(x):
    if not x:
        return "?"
    key = "debugString_{}".format(type(x).__name__)
    if key in globals():
        return globals()[key](x)
    else:
        return displayStructure(x)


_designationTypeLookup = {
    "NoneType" : "Nil",
    "Boolean" : "Truth Value",
    "bool" : "Truth Value",
    "Integer" : "Number",
    "int" : "Number",
    "Real" : "Real Number",
    "float" : "Real Number",
    "str" : "Word",
    "String" : "Word",
    "MetaCop" : "Behavior",
    "Cop" : "Behavior",
    "Do" : "Process",
    "Cell" : "Structure",
}

_structureTypeLookup = {
    "NoneType" : "Nil",
    "bool" : "Boolean",
    "int" : "Integer",
    "str" : "String",
    "float" : "Real",
}

def displayDesignation(x):
    t = None
    if isinstance(x, M.Cell):
        if x.cellType:
            t = x.cellType.human.name
        if (not t) or (t == 'Generic'):
            t = type(x.data).__name__
        if hasattr(x.data, 'fsType'): # is it a model object?
            d = "..."
            if isinstance(x.data, M.Cell):
                st = type(x.data.data).__name__
                d = _structureTypeLookup.get(st, st) + "..."
        elif (x.data == None):
            d = 'Nil'
        else:
            d = str(x.data)
    if not t:
        #print(t, x)
        return "{Undefined designation}"
    return "{{{}:{}}}".format(_designationTypeLookup.get(t, t), d)
