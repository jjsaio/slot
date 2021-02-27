
from . import model as M
from .context import Context


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
        return ctx.addNamedSlot(name, M.Slot(slotType = typeType, human = M.Human(name = name, displayType = displayType or name)))

    generic = addType('Generic', displayType = '*')
    nat = addType('_Native', displayType = 'scalar')
    integer = addType('Integer', typeType = nat)
    addType('Slot', typeType = nat)
    addType('MetaSlot', typeType = nat)
    addType('Slex', typeType = nat)
    addType('MetaSlex', typeType = nat)
    slop = addType('Slop', typeType = nat)

    def addBuiltin(name, handler, types):
        ctx.addNamedSlot(name, M.Slot(slotType = slop,
                                      data = M.Slop(params = [ M.MetaSlot(slotType = t) for t in types ],
                                                    native = handler)))

    addBuiltin('plus', _Integer_plus, [ integer, integer, integer ])
    addBuiltin('Slot_copy', _Slot_copy, [ generic, generic ])

    return ctx
