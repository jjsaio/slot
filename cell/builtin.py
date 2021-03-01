
from . import model as M
from .display import displayDesignation
from .namespace import Namespace
from .util import prettyJson


def _Integer_plus(ctx):
    # these asserts should be done by _execute, just doing here for illustration
    if False:
        do = ctx.node.do
        cop = do.op
        assert(_Integer_plus == cop.native)
        assert(3 == len(do.args))
        for i in range(len(cop.params)):
            assert(cop.params[i].cellType == do.args[i].cellType)
    dst, a, b = ctx.node.do.args
    dst.data = a.data + b.data

def _Integer_minus(ctx):
    dst, a, b = ctx.node.do.args
    dst.data = a.data - b.data

def _Integer_times(ctx):
    dst, a, b = ctx.node.do.args
    dst.data = a.data * b.data

def _Boolean_greaterThan(ctx):
    dst, a, b = ctx.node.do.args
    dst.data = (a.data > b.data)

def _Cell_copy(ctx):
    do = ctx.node.do
    dst, src = do.args
    if not (isinstance(dst.data, M.Cell) and isinstance(src.data, M.Cell)): # should have been type-verified by _execute, can nuke once good
        raise Exception("Attempt to copy non-cells: `{}` <- `{}`".format(displayDesignation(dst), displayDesignation(src)))
    # TODO: runtime type compat? better of course if it's link-time...
    dst.data.data = src.data.data

def _Generic_up(ctx):
    do = ctx.node.do
    source, cell = do.args
    cell.data = source

def _Generic_print(ctx):
    do = ctx.node.do
    cell = do.args[0]
    print(cell.data)

def _Cell_down(ctx):
    do = ctx.node.do
    cell, dest = do.args
    if not isinstance(cell.data, M.Cell):
        raise Exception("Attempt to `down` non-structure `{}`".format(displayDesignation(cell)))
    # TODO: runtime type compat?
    dest.data = cell.data.data

def _Cop_execute(ctx):
    do = ctx.node.do
    cop = do.args[0]
    assert(isinstance(cop.data, M.Cop))
    ctx.interpreter.executor.execute(M.Do(op = cop.data))

def _Cop_executeIf(ctx):
    do = ctx.node.do
    cop, cond = do.args
    if cond.data:
        assert(isinstance(cop.data, M.Cop))
        ctx.interpreter.execute(M.Do(op = cop.data))

def _Cop_executeIfElse(ctx):
    do = ctx.node.do
    ifCop, cond, elCop = do.args
    execCop = ifCop if cond.data else elCop
    assert(isinstance(execCop.data, M.Cop))
    ctx.interpreter.execute(M.Do(op = execCop.data))

def _ExecutionContext_current(ctx):
    do = ctx.node.do
    dest = do.args[0]
    # TODO: runtime type compat? better of course if it's link-time...
    dest.data = ctx

def _ExecutionNode_current(ctx):
    do = ctx.node.do
    dest = do.args[0]
    # TODO: runtime type compat? better of course if it's link-time...
    dest.data = ctx.node

def _ExecutionNode_printDoStack(ctx):
    do = ctx.node.do
    cell = do.args[0]
    if not isinstance(cell.data, M.ExecutionNode):
        raise Exception("Not an ExecutionNode: `{}`".format(displayDesignation(cell)))
    _printDoStack(ctx, startNode = cell.data)

def _ExecutionNode_printNextDos(ctx):
    do = ctx.node.do
    cell = do.args[0]
    if not isinstance(cell.data, M.ExecutionNode):
        raise Exception("Not an ExecutionNode: `{}`".format(displayDesignation(cell)))
    _printNextDos(ctx, startNode = cell.data)

def _printDoStack(ctx, startNode = None):
    cur = startNode or ctx.node
    level = 0
    while cur:
        print("  [{}] {}".format(level, cur.do.op.op.human.name))
        level += 1
        cur = cur.parent

def _printNextDos(ctx, startNode = None):
    cur = startNode or ctx.node
    while cur:
        if cur.executed:
            prefix = " \-*"
        elif cur == ctx.node:
            prefix = "  @ "
        else:
            prefix = " \->"
        print("  {} {}".format(prefix, cur.do.op.op.human.name))
        cur = cur.next


def builtinNamespace():
    ns = Namespace()

    typeType = M.CellType(human = M.Human(name = 'Type'))

    def addType(name):
        st = M.CellType(human = M.Human(name = name))
        s = M.Cell(cellType = typeType, data = st, human = st.human)
        ns.addNamedCell(name, M.MetaCell(cellType = s.cellType, concrete = s, human = s.human))
        return st

    generic = addType('Generic')
    addType('Nil')
    boolean = addType('Boolean')
    integer = addType('Integer')
    addType('Real')
    addType('String')
    cell = addType('Cell')
    addType('MetaCell')
    addType('Do')
    addType('MetaDo')
    addType('Cop')
    cop = addType('MetaCop')
    exctx = addType('ExecutionContext')
    exnode = addType('ExecutionNode')

    def addBuiltin(name, handler, params):
        h = M.Human(name = name)
        s = M.Cell(cellType = cop,
                   data = M.MetaCop(params = [ M.MetaCell(cellType = t, human = M.Human(name = n)) for (n, t) in params ],
                                     native = handler,
                                     human = h),
                   human = h)
        ns.addNamedCell(name, M.MetaCell(cellType = s.cellType, concrete = s, human = h))
        return s

    addBuiltin('Boolean_greaterThan', _Boolean_greaterThan, [ ("b", boolean), ("x", integer), ("y", integer) ])
    addBuiltin('Integer_plus', _Integer_plus, [ ("sum", integer), ("x", integer), ("y", integer) ])
    addBuiltin('Integer_minus', _Integer_minus, [ ("difference", integer), ("x", integer), ("y", integer) ])
    addBuiltin('Integer_times', _Integer_times, [ ("product", integer), ("x", integer), ("y", integer) ])
    addBuiltin('Cell_copy', _Cell_copy, [ ("dest", cell), ("source", cell) ])
    addBuiltin('Generic_up', _Generic_up, [ ("source", generic), ("cell", cell) ])
    addBuiltin('Generic_print', _Generic_print, [ ("item", generic) ])
    addBuiltin('Cell_down', _Cell_down, [ ("cell", cell), ("dest", generic) ])
    addBuiltin('Cop_execute', _Cop_execute, [ ( "cop", cop ) ])
    addBuiltin('Cop_executeIf', _Cop_executeIf, [ ( "cop", cop ), ("cond", boolean ) ])
    addBuiltin('Cop_executeIfElse', _Cop_executeIfElse, [ ( "ifcop", cop ), ("cond", boolean ), ( "elcop", cop ) ])
    addBuiltin('ExecutionContext_current', _ExecutionContext_current, [ ( "ctx", exctx ) ])
    addBuiltin('ExecutionNode_current', _ExecutionNode_current, [ ( "node", exnode ) ])
    addBuiltin('ExecutionNode_printDoStack', _ExecutionNode_printDoStack, [ ( "node", exnode ) ])
    addBuiltin('ExecutionNode_printNextDos', _ExecutionNode_printNextDos, [ ( "node", exnode ) ])
    addBuiltin('_printDoStack', _printDoStack, [ ])
    addBuiltin('_printNextDos', _printNextDos, [ ])

    return ns
