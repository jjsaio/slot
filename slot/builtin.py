
from . import model as M
from .context import Context
from .display import displayDesignation
from .util import prettyJson


def _Integer_plus(ctx):
    slex = ctx.node.slex
    slop = slex.op
    # these asserts should be done by _execute, just doing here for illustration
    if False:
        assert(_Integer_plus == slop.native)
        assert(3 == len(slex.args))
        for i in range(len(slop.params)):
            assert(slop.params[i].slotType == slex.args[i].slotType)
    dst, a, b = slex.args
    dst.data = a.data + b.data

def _Slot_copy(ctx):
    slex = ctx.node.slex
    dst, src = slex.args
    if not (isinstance(dst.data, M.Slot) and isinstance(src.data, M.Slot)): # should have been type-verified by _execute, can nuke once good
        raise Exception("Attempt to copy non-slots: `{}` <- `{}`".format(displayDesignation(dst), displayDesignation(src)))
    # TODO: runtime type compat? better of course if it's link-time...
    dst.data.data = src.data.data

def _Generic_up(ctx):
    slex = ctx.node.slex
    source, slot = slex.args
    slot.data = source

def _Slot_down(ctx):
    slex = ctx.node.slex
    slot, dest = slex.args
    if not isinstance(slot.data, M.Slot):
        raise Exception("Attempt to `down` non-structure `{}`".format(displayDesignation(slot)))
    # TODO: runtime type compat?
    dest.data = slot.data.data

def _Slop_execute(ctx):
    slex = ctx.node.slex
    slop = slex.args[0]
    assert(isinstance(slop.data, M.Slop))
    ctx.interpreter.executor.executeSlex(M.Slex(op = slop.data))

def _Slop_execute_if(ctx):
    slex = ctx.node.slex
    slop, cond = slex.args
    if cond.data:
        assert(isinstance(slop.data, M.Slop))
        ctx.interpreter.executor.executeSlex(M.Slex(op = slop.data))

def _ExecutionContext_current(ctx):
    slex = ctx.node.slex
    dest = slex.args[0]
    # TODO: runtime type compat? better of course if it's link-time...
    dest.data = ctx

def _ExecutionNode_current(ctx):
    slex = ctx.node.slex
    dest = slex.args[0]
    # TODO: runtime type compat? better of course if it's link-time...
    dest.data = ctx.node

def _ExecutionNode_printStack(ctx):
    slex = ctx.node.slex
    slot = slex.args[0]
    if not isinstance(slot.data, M.ExecutionNode):
        raise Exception("Not an ExecutionNode: `{}`".format(displayDesignation(slot)))
    _printStack(ctx, startNode = slot.data)

def _ExecutionNode_printNextInstructions(ctx):
    slex = ctx.node.slex
    slot = slex.args[0]
    if not isinstance(slot.data, M.ExecutionNode):
        raise Exception("Not an ExecutionNode: `{}`".format(displayDesignation(slot)))
    _printNextInstructions(ctx, startNode = slot.data)

def _printStack(ctx, startNode = None):
    cur = startNode or ctx.node
    level = 0
    while cur:
        print("  [{}] {}".format(level, cur.slex.op.human.name))
        level += 1
        cur = cur.parent

def _printNextInstructions(ctx, startNode = None):
    cur = startNode or ctx.node
    while cur:
        if cur.executed:
            prefix = " \-*"
        elif cur == ctx.node:
            prefix = "  @ "
        else:
            prefix = " \->"
        print("  {} {}".format(prefix, cur.slex.op.human.name))
        cur = cur.next


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
    exctx = addType('ExecutionContext')
    exnode = addType('ExecutionNode')

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
    addBuiltin('ExecutionContext_current', _ExecutionContext_current, [ ( "ctx", exctx ) ])
    addBuiltin('ExecutionNode_current', _ExecutionNode_current, [ ( "node", exnode ) ])
    addBuiltin('ExecutionNode_printStack', _ExecutionNode_printStack, [ ( "node", exnode ) ])
    addBuiltin('ExecutionNode_printNextInstructions', _ExecutionNode_printNextInstructions, [ ( "node", exnode ) ])
    addBuiltin('_printStack', _printStack, [ ])
    addBuiltin('_printNextInstructions', _printNextInstructions, [ ])

    return ctx
