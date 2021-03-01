
import lark

from . import model as M
from .logging import LoggingClass


class Definer(LoggingClass):

    def __init__(self):
        LoggingClass.__init__(self)
        pass

    def define(self, parseTree):
        assert("ParseTree" == parseTree.__class__.__name__)
        if parseTree.parser.shortcuts:
            return ExtendedDefinitionMaker().transform(parseTree.tree)
        else:
            return KernelDefinitionMaker().transform(parseTree.tree)


class KernelDefinitionMaker(lark.Transformer, LoggingClass):

    #def _call_userfunc(self, tree, children):
    #    print("CUF", tree)
    #    return lark.Transformer._call_userfunc(self, tree, children)

    def __init__(self):
        lark.Transformer.__init__(self)
        LoggingClass.__init__(self)
        #self.setLevelDebug()

    def _simple(self, args):
        assert(1 == len(args))
        return args[0]

    start = _simple

    def interactive(self, args):
        assert(1 == len(args))
        # always returning a list simplifies interactive-mode impl
        if isinstance(args[0], list):
            return args[0]
        else:
            return [ args[0] ]

               
    def interpreter(self, args):
        assert(1 == len(args))
        assert(isinstance(args[0], list))
        sd = self.cop([ [], args[0] ])
        assert(isinstance(sd, M.CopDef))
        return sd

    #------- kernel defs

    def _flattenSteps(self, args):
        steps = []
        for arg in args:
            if isinstance(arg, list):
                steps += arg
            else:
                steps.append(arg)
        return steps

    def cop(self, args):
        copDef = M.CopDef(params = args[0])
        for step in self._flattenSteps(args[1]):
            if isinstance(step, M.CellDef):
                copDef.locals.append(step)
            else:
                assert(isinstance(step, M.DoDef))
                copDef.steps.append(step)
        for s in copDef.params + copDef.locals:
            assert(isinstance(s, M.CellDef))
        return copDef

    def cop_params(self, args):
        for arg in args:
            assert(arg.name)
        return args

    def cop_body(self, args):
        return [ x for x in args if x ] # drops comments

    def cop_step(self, args):
        assert(1 == len(args))
        assert(isinstance(args[0], M.CellDef) or isinstance(args[0], M.DoDef) or isinstance(args[0], list) or (not args[0]))
        return args[0]

    def comment(self, args):
        return None


    def do(self, args):
        assert(1 == len(args))
        assert(isinstance(args[0], M.DoDef))
        return args[0]

    def do_call(self, args):
        assert(2 == len(args))
        assert(isinstance(args[0], M.CellRef))
        assert(isinstance(args[1], list))
        for arg in args[1]:
            assert(isinstance(arg, M.CellRef))
        return M.DoDef(op = args[0], args = args[1])

    def do_op(self, args):
        assert(1 == len(args))
        assert(isinstance(args[0], M.CellRef))
        return args[0]

    def do_args(self, args):
        return args


    def cell_spec(self, args):
        assert(len(args) >= 1  and  len(args) <= 2)
        assert(isinstance(args[0], str))
        cellDef = M.CellDef(name = args[0])
        if len(args) > 1:
            assert(isinstance(args[1], str))
            cellDef.cellType = args[1]
        return cellDef

    def cell_def(self, args):
        for arg in args:
            assert(isinstance(arg, M.CellDef))
        if len(args) == 2:
            spec, const = args
            assert((not spec.cellType) or (spec.cellType == const.cellType))
            assert(not const.name)
            const.name = spec.name
            return const
        else:
            return args[0]

    def cell(self, args):
        assert(1 == len(args))
        assert(isinstance(args[0], M.CellRef))
        return args[0]

    def cell_name(self, args):
        assert(1 == len(args))
        return args[0].value

    def cell_ref(self, args):
        assert(1 == len(args))
        assert(isinstance(args[0], str))
        return M.CellRef(name = args[0])


    #------- constants

    def constant(self, args):
        assert(1 == len(args))
        if isinstance(args[0], M.CopDef):
            return M.CellDef(cop = args[0])
        sd = args[0]
        assert(isinstance(sd, M.CellDef))
        assert(sd.constant and isinstance(sd.constant, list)) # this is so we can use `if sd.constant` more clearly
        return sd

    def _token_dispatch(self, tokenClass, token):
        return getattr(self, "_{}_{}".format(tokenClass, token.type))(token.value)
        
    def literal(self, args):
        assert(1 == len(args))
        return self._token_dispatch("literal", args[0])

    def _literal_INTEGER(self, val):
        return M.CellDef(cellType = "Integer", constant = [ int(val) ])

    def _literal_STRING(self, val):
        assert((val[0] in [ '"', "'" ]) and (val[-1] in [ '"', "'" ]))
        return M.CellDef(cellType = "String", constant = [ val[1:-1] ])

    def _literal_BOOLEAN(self, val):
        return M.CellDef(cellType = "Boolean", constant = [ { "$t" : True, "$f" : False}[val] ])

    def _literal_REAL(self, val):
        return M.CellDef(cellType = "Real", constant = [ float(val) ])

    def _literal_NIL(self, val):
        return M.CellDef(cellType = "Nil", constant = [ None ])



# syntactic shortcuts, etc
class ExtendedDefinitionMaker(KernelDefinitionMaker):

    def __init__(self):
        KernelDefinitionMaker.__init__(self)

    def _simple(self, args):
        assert(1 == len(args))
        return args[0]

    syntactic_shortcut = _simple

    #------- {a,de}scension

    def up(self, args):
        assert(1 == len(args))
        ref = args[0]
        assert(isinstance(ref, M.CellRef))
        sd = M.CellDef(cellType = "Cell")
        do = M.DoDef(op = M.CellRef(name = "Generic_up"),
                         args = [ ref, M.CellRef(cell = sd, name = "_↑{}_".format(ref.name)) ])
        return [ sd, do ]

    def down(self, args):
        assert(1 == len(args))
        ref = args[0]
        assert(isinstance(ref, M.CellRef))
        sd = M.CellDef(cellType = "Generic")
        do = M.DoDef(op = M.CellRef(name = "Cell_down"),
                         args = [ ref, M.CellRef(cell = sd, name = "_↓{}_".format(ref.name)) ])
        return [ sd, do ]


    #------- assignment / ctor

    def assignment(self, args):
        assert(2 == len(args))
        assert(isinstance(args[0], M.CellRef))
        assert(isinstance(args[1], M.CellRef))
        destAscension = self.up([ args[0] ])
        sourceAscension = self.up([ args[1] ])
        do = M.DoDef(op = M.CellRef(name = "Cell_copy"),
                         args = [ M.CellRef(cell = destAscension[0]), M.CellRef(cell = sourceAscension[0]) ])
        return destAscension + sourceAscension + [ do ]

    def constructor(self, args):
        assert(2 == len(args))
        assert(isinstance(args[0], M.CellDef))
        assert(isinstance(args[1], M.CellRef))
        return [ args[0] ] + self.assignment([ M.CellRef(cell = args[0]), args[1] ])
