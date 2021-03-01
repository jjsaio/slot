
from . import model as M
from .display import displayDesignation
from .namespace import Namespace
from .util import prettyJson


def _Integer_plus(ctx):
    # these asserts should be done by _execute, just doing here for illustration
    if False:
        slex = ctx.node.slex
        slop = slex.op
        assert(_Integer_plus == slop.native)
        assert(3 == len(slex.args))
        for i in range(len(slop.params)):
            assert(slop.params[i].slotType == slex.args[i].slotType)
    dst, a, b = ctx.node.slex.args
    dst.data = a.data + b.data

def _Integer_minus(ctx):
    dst, a, b = ctx.node.slex.args
    dst.data = a.data - b.data

def _Integer_times(ctx):
    dst, a, b = ctx.node.slex.args
    dst.data = a.data * b.data

def _Boolean_greaterThan(ctx):
    dst, a, b = ctx.node.slex.args
    dst.data = (a.data > b.data)

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

def _Generic_print(ctx):
    slex = ctx.node.slex
    slot = slex.args[0]
    print(slot.data)

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

def _Slop_executeIf(ctx):
    slex = ctx.node.slex
    slop, cond = slex.args
    if cond.data:
        assert(isinstance(slop.data, M.Slop))
        ctx.interpreter.excute(M.Slex(op = slop.data))

def _Slop_executeIfElse(ctx):
    slex = ctx.node.slex
    ifSlop, cond, elSlop = slex.args
    execSlop = ifSlop if cond.data else elSlop
    assert(isinstance(execSlop.data, M.Slop))
    ctx.interpreter.execute(M.Slex(op = execSlop.data))

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
        print("  {} {}".format(prefix, cur.slex.op.op.human.name))
        cur = cur.next


def builtinNamespace():
    ns = Namespace()

    typeType = M.SlotType(human = M.Human(name = 'Type'))

    def addType(name):
        st = M.SlotType(human = M.Human(name = name))
        s = M.Slot(slotType = typeType, data = st, human = st.human)
        ns.addNamedSlot(name, M.MetaSlot(slotType = s.slotType, concrete = s, human = s.human))
        return st

    generic = addType('Generic')
    addType('Nil')
    boolean = addType('Boolean')
    integer = addType('Integer')
    addType('Real')
    addType('String')
    slot = addType('Slot')
    addType('MetaSlot')
    addType('Slex')
    addType('MetaSlex')
    addType('Slop')
    slop = addType('MetaSlop')
    exctx = addType('ExecutionContext')
    exnode = addType('ExecutionNode')

    def addBuiltin(name, handler, params):
        h = M.Human(name = name)
        s = M.Slot(slotType = slop,
                   data = M.MetaSlop(params = [ M.MetaSlot(slotType = t, human = M.Human(name = n)) for (n, t) in params ],
                                     native = handler,
                                     human = h),
                   human = h)
        ns.addNamedSlot(name, M.MetaSlot(slotType = s.slotType, concrete = s, human = h))
        return s

    addBuiltin('Boolean_greaterThan', _Boolean_greaterThan, [ ("b", boolean), ("x", integer), ("y", integer) ])
    addBuiltin('Integer_plus', _Integer_plus, [ ("sum", integer), ("x", integer), ("y", integer) ])
    addBuiltin('Integer_minus', _Integer_minus, [ ("difference", integer), ("x", integer), ("y", integer) ])
    addBuiltin('Integer_times', _Integer_times, [ ("product", integer), ("x", integer), ("y", integer) ])
    addBuiltin('Slot_copy', _Slot_copy, [ ("dest", slot), ("source", slot) ])
    addBuiltin('Generic_up', _Generic_up, [ ("source", generic), ("slot", slot) ])
    addBuiltin('Generic_print', _Generic_print, [ ("item", generic) ])
    addBuiltin('Slot_down', _Slot_down, [ ("slot", slot), ("dest", generic) ])
    addBuiltin('Slop_execute', _Slop_execute, [ ( "slop", slop ) ])
    addBuiltin('Slop_executeIf', _Slop_executeIf, [ ( "slop", slop ), ("cond", boolean ) ])
    addBuiltin('Slop_executeIfElse', _Slop_executeIfElse, [ ( "ifslop", slop ), ("cond", boolean ), ( "elslop", slop ) ])
    addBuiltin('ExecutionContext_current', _ExecutionContext_current, [ ( "ctx", exctx ) ])
    addBuiltin('ExecutionNode_current', _ExecutionNode_current, [ ( "node", exnode ) ])
    addBuiltin('ExecutionNode_printStack', _ExecutionNode_printStack, [ ( "node", exnode ) ])
    addBuiltin('ExecutionNode_printNextInstructions', _ExecutionNode_printNextInstructions, [ ( "node", exnode ) ])
    addBuiltin('_printStack', _printStack, [ ])
    addBuiltin('_printNextInstructions', _printNextInstructions, [ ])

    return ns
