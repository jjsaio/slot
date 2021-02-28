
from . import model as M
from .context import Context
from .util import prettyJson


def _Integer_plus(slex, executor):
    slop = slex.op
    # these asserts should be done by _execute, just doing here for illustration
    if False:
        assert(_Integer_plus == slop.native)
        assert(3 == len(slex.args))
        for i in range(len(slop.params)):
            assert(slop.params[i].slotType == slex.args[i].slotType)
    slex.args[0].data = slex.args[1].data + slex.args[2].data

def _Slot_copy(slex, executor):
    slex.args[0].data = slex.args[1].data

def _Slop_execute(slex, executor):
    slop = slex.args[0].data
    assert(isinstance(slop, M.Slop))
    executor.execute(M.Slex(op = slop))

def _Slop_execute_if(slex, executor):
    if slex.args[1].data:
        slop = slex.args[0].data
        assert(isinstance(slop, M.Slop))
        executor.execute(M.Slex(op = slop))


def builtinContext():
    ctx = Context()

    typeType = M.SlotType(human = M.Human(name = 'Type'))

    def addType(name, displayType = None):
        st = M.SlotType(human = M.Human(name = name, displayType = displayType))
        s = M.Slot(slotType = typeType, data = st, human = st.human)
        ctx.addNamedSlot(name, M.MetaSlot(slotType = s.slotType, concrete = s, human = s.human))
        return st

    generic = addType('Generic', displayType = '*')
    addType('Nil')
    boolean = addType('Boolean')
    integer = addType('Integer')
    addType('Real')
    addType('String')
    addType('Slot')
    addType('MetaSlot')
    addType('Slex')
    addType('MetaSlex')
    slop = addType('Slop')

    def addBuiltin(name, handler, params):
        h = M.Human(name = name)
        s = M.Slot(slotType = slop,
                   data = M.Slop(params = [ M.MetaSlot(slotType = t, human = M.Human(name = n)) for (n, t) in params ],
                                 native = handler,
                                 human = h),
                   human = h)
        ctx.addNamedSlot(name, M.MetaSlot(slotType = s.slotType, concrete = s, human = h))
        return s

    addBuiltin('plus', _Integer_plus, [ ("sum", integer), ("x", integer), ("y", integer) ])

    addBuiltin('Slot_copy', _Slot_copy, [ ("dest", generic), ("source", generic) ])
    addBuiltin('Slop_execute', _Slop_execute, [ ( "slop", slop ) ])
    addBuiltin('Slop_execute_if', _Slop_execute_if, [ ( "slop", slop ), ("cond", boolean ) ])

    return ctx
