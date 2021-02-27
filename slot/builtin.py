
from . import model as M
from .context import Context
from .util import prettyJson


def _Integer_plus(slex):
    slop = slex.op
    # these asserts should be done by _execute, just doing here for illustration
    if False:
        assert(_Integer_plus == slop.native)
        assert(3 == len(slex.args))
        for i in range(len(slop.params)):
            assert(slop.params[i].slotType == slex.args[i].slotType)
    slex.args[0].data = slex.args[1].data + slex.args[2].data

def _Slot_copy(slex):
    slex.args[0].data = slex.args[1].data


def builtinContext():
    ctx = Context()
    def addType(name, displayType = None, typeType = None):
        s = M.Slot(slotType = typeType, human = M.Human(name = name, displayType = displayType or name))
        ctx.addNamedSlot(name, M.MetaSlot(slotType = s.slotType, concrete = s))
        return s

    generic = addType('Generic', displayType = '*')
    nat = addType('_Native', displayType = 'scalar')
    integer = addType('Integer', typeType = nat)
    integer = addType('Boolean', typeType = nat)
    integer = addType('Real', typeType = nat)
    integer = addType('String', typeType = nat)
    addType('Slot', typeType = nat)
    addType('MetaSlot', typeType = nat)
    addType('Slex', typeType = nat)
    addType('MetaSlex', typeType = nat)
    slop = addType('Slop', typeType = nat)

    def addBuiltin(name, handler, params):
        s = M.Slot(slotType = slop,
                   data = M.Slop(params = [ M.MetaSlot(slotType = t, human = M.Human(name = n)) for (n, t) in params ],
                                 native = handler))
        ctx.addNamedSlot(name, M.MetaSlot(slotType = s.slotType, concrete = s))
        return s

    addBuiltin('plus', _Integer_plus, [ ("sum", integer), ("x", integer), ("y", integer) ])
    addBuiltin('Slot_copy', _Slot_copy, [ ("dest", generic), ("source", generic) ])
    return ctx
