
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
        sd = self.slop([ [], args[0] ])
        assert(isinstance(sd, M.SlopDef))
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

    def slop(self, args):
        slopDef = M.SlopDef(params = args[0])
        for step in self._flattenSteps(args[1]):
            if isinstance(step, M.SlotDef):
                slopDef.locals.append(step)
            else:
                assert(isinstance(step, M.SlexDef))
                slopDef.steps.append(step)
        for s in slopDef.params + slopDef.locals:
            assert(isinstance(s, M.SlotDef))
            assert(s.name)
        return slopDef

    def slop_params(self, args):
        for arg in args:
            assert(arg.name)
        return args

    def slop_body(self, args):
        return args

    def slop_step(self, args):
        assert(1 == len(args))
        assert(isinstance(args[0], M.SlotDef) or isinstance(args[0], M.SlexDef) or isinstance(args[0], list))
        return args[0]


    def slex(self, args):
        assert(1 == len(args))
        assert(isinstance(args[0], M.SlexDef))
        return args[0]

    def slex_call(self, args):
        assert(2 == len(args))
        assert(isinstance(args[0], M.SlotRef))
        return M.SlexDef(op = args[0], args = args[1])

    def slex_op(self, args):
        assert(1 == len(args))
        assert(isinstance(args[0], M.SlotRef))
        return args[0]

    def slex_args(self, args):
        return args


    def slot_spec(self, args):
        assert(len(args) >= 1  and  len(args) <= 2)
        assert(isinstance(args[0], str))
        slotDef = M.SlotDef(name = args[0])
        if len(args) > 1:
            assert(isinstance(args[1], str))
            slotDef.slotType = args[1]
        return slotDef

    def slot_def(self, args):
        assert(len(args) == 1)
        sd = args[0]
        assert(isinstance(sd, M.SlotDef))
        return sd

    def slot(self, args):
        assert(1 == len(args))
        assert(isinstance(args[0], M.SlotRef))
        return args[0]

    def slot_name(self, args):
        assert(1 == len(args))
        return args[0].value


    def slop_ref(self, args):
        assert(isinstance(args[0], M.SlopDef))
        return M.SlotRef(slop = args[0])

    def slot_ref(self, args):
        assert(1 == len(args))
        assert(isinstance(args[0], str))
        return M.SlotRef(name = args[0])


    #------- constants

    def constant(self, args):
        assert(1 == len(args))
        assert(isinstance(args[0], M.SlotDef))
        return M.SlotRef(slot = args[0])

    def _token_dispatch(self, tokenClass, token):
        return getattr(self, "_{}_{}".format(tokenClass, token.type))(token.value)
        
    def literal(self, args):
        assert(1 == len(args))
        return self._token_dispatch("literal", args[0])

    def _literal_INTEGER(self, val):
        sd = M.SlotDef(slotType = "Integer")
        sd.constant = int(val) # can't use initializer b/c gencode with Object type uses "or None"
        return sd

    def _literal_STRING(self, val):
        return M.SlotDef(slotType = "String", constant = str(val))



# syntactic shortcuts, etc
class ExtendedDefinitionMaker(KernelDefinitionMaker):

    def __init__(self):
        KernelDefinitionMaker.__init__(self)

    def _simple(self, args):
        assert(1 == len(args))
        return args[0]

    syntactic_shortcut = _simple

    def assignment(self, args):
        assert(2 == len(args))
        assert(isinstance(args[0], M.SlotRef))
        assert(isinstance(args[1], M.SlotRef))
        return M.SlexDef(op = M.SlotRef(name = "Slot_copy"), args = args)

    def constructor(self, args):
        assert(2 == len(args))
        assert(isinstance(args[0], M.SlotDef))
        assert(isinstance(args[1], M.SlotRef))
        return [ args[0], self.assignment([ M.SlotRef(name = args[0].name), args[1] ]) ]
