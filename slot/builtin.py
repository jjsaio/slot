
from . import model as M
from .context import Context
from .display import displayDesignation
from .util import prettyJson


def _Integer_plus(slex, executor):
    slop = slex.op
    # these asserts should be done by _execute, just doing here for illustration
    if False:
        assert(_Integer_plus == slop.native)
        assert(3 == len(slex.args))
        for i in range(len(slop.params)):
            assert(slop.params[i].slotType == slex.args[i].slotType)
    dst, a, b = slex.args
    dst.data = a.data + b.data

def _Slot_copy(slex, executor):
    dst, src = slex.args
    if not (isinstance(dst.data, M.Slot) and isinstance(src.data, M.Slot)): # should have been type-verified by _execute, can nuke once good
        raise Exception("Attempt to copy non-slots: `{}` <- `{}`".format(displayDesignation(dst), displayDesignation(src)))
    # TODO: runtime type compat? better of course if it's link-time...
    dst.data.data = src.data.data

def _Generic_up(slex, executor):
    source, slot = slex.args
    slot.data = source

def _Slot_down(slex, executor):
    slot, dest = slex.args
    if not isinstance(slot.data, M.Slot):
        raise Exception("Attempt to `down` non-structure `{}`".format(displayDesignation(slot)))
    # TODO: runtime type compat?
    dest.data = slot.data.data

def _Slop_execute(slex, executor):
    slop = slex.args[0]
    assert(isinstance(slop.data, M.Slop))
    executor.execute(M.Slex(op = slop.data))

def _Slop_execute_if(slex, executor):
    slop, cond = slex.args
    if cond.data:
        assert(isinstance(slop.data, M.Slop))
        executor.execute(M.Slex(op = slop.data))


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
    slot = addType('Slot')
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
    addBuiltin('Slot_copy', _Slot_copy, [ ("dest", slot), ("source", slot) ])
    addBuiltin('Generic_up', _Generic_up, [ ("source", generic), ("slot", slot) ])
    addBuiltin('Slot_down', _Slot_down, [ ("slot", slot), ("dest", generic) ])
    addBuiltin('Slop_execute', _Slop_execute, [ ( "slop", slop ) ])
    addBuiltin('Slop_execute_if', _Slop_execute_if, [ ( "slop", slop ), ("cond", boolean ) ])

    return ctx
