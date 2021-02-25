
import lark

from .fs import fs
from .logging import LoggingClass
from .util import moduleFile, strWithFileAtPath, prettyJson

from . import model as M


class ParseResult(object):

    def __init__(self, parser, tree):
        self.parser = parser
        self.tree = tree

    def visualizeTree(self, png_path = None, show = False):
        from lark.tree import pydot__tree_to_png
        png_path = png_path or "/tmp/slot.png"
        pydot__tree_to_png(self.tree, png_path)
        if show:
            import subprocess
            subprocess.call(['open', png_path])

    def structure(self, env):
        return StructureMaker(env).transform(self.tree)

    def command(self, env):
        return CommandMaker(env).transform(self.tree)


class Parser(object):

    def __init__(self):
        self.grammar = strWithFileAtPath(moduleFile(__file__, 'slot.g'))
        self.parser = lark.Lark(self.grammar)

    def parse(self, text, raise_if_not_parseable = True):
        try:
            return ParseResult(self, self.parser.parse(text))
        except lark.ParseError:
            if raise_if_not_parseable:
                raise
            return None

    def parses(self, text):
        return bool(self.parse(text, raise_if_not_parseable = False))


class StructureMaker(lark.Transformer, LoggingClass):

    #def _call_userfunc(self, tree, children):
    #    print("CUF", tree)
    #    return lark.Transformer._call_userfunc(self, tree, children)
    def __init__(self, env):
        lark.Transformer.__init__(self)
        LoggingClass.__init__(self)
        #self.setLevelDebug()
        self.env = env

    def _simple(self, args):
        assert(1 == len(args))
        return args[0]

    start = _simple

    def _fixRefs(self, struc, env):
        assert(struc.fsType in [ fs.Slot, fs.SlotRef, fs.Slex, fs.Slop ])
        return getattr(self, "_fixRefs_{}".format(fs.toString(struc.fsType)))(struc, env)

    def _fixRefs_Slot(self, slot, env):
        assert(isinstance(slot, M.Slot))
        if slot.data and hasattr(slot.data, 'fsType') and (slot.data.fsType in [ fs.Slot, fs.SlotRef, fs.Slex, fs.Slop ]):
            slot.data = self._fixRefs(slot.data, env)
        return slot

    def _fixRefs_SlotRef(self, ref, env):
        if not ref.slot:
            if not env.hasSlotNamed(ref.name):
                raise Exception("Unbound slot reference: `{}`".format(ref.name))
            ref.slot = env.slotNamed(ref.name)
            assert(ref.slot.human.name)
        return ref.slot

    def _fixRefs_Slex(self, slex, env):
        assert(isinstance(slex, M.Slex))
        self._fixRefs_Slot(slex.op, env)
        slex.args = [ self._fixRefs(x, env) for x in slex.args ]
        return slex

    def _fixRefs_Slop(self, slop, env):
        assert(isinstance(slop, M.Slop))
        slopEnv = env.derive()
        for param in slop.params:
            if param.human and param.human.name:
                assert(isinstance(param.data, M.Slot)) # this must be a metaslot
                slopEnv.addNamedSlot(param.data.human.name, param)
            else:
                # builtins may not have named slots
                slopEnv.addSlot(param)
        for local in slop.locals:
            assert(isinstance(local.data, M.Slot)) # this must be a metaslot
            slopEnv.addNamedSlot(local.data.human.name, local)
        self.debug("slop derived env:", slopEnv.dump())
        for step in slop.steps:
            self._fixRefs_Slex(step, slopEnv)
        return slop
            
    def structure(self, args):
        assert(1 == len(args))
        return self._fixRefs(args[0], self.env)

    def slot_def(self, args):
        assert(len(args) >= 1)
        slot = args[0]
        if len(args) > 1:
            # TODO: check slot-type compatbility
            # TODO: if slot.type is generic, set it to args[1].type (?)
            slot.data = args[1].data
        return self.env.addNamedSlot(slot.human.name, slot)

    def slot_spec(self, args):
        assert(len(args) >= 1  and  len(args) <= 3)
        name = args[0]
        slot = M.Slot(human = M.Human(name = name))
        if len(args) > 1:
            slotType = args[1]
            slotType = {
                "Integer" : "_Integer",
                "int" : "_Integer",
                "String" : "_String",
                "str" : "_String",
            }.get(slotType, slotType)
            if not self.env.hasSlotNamed(slotType):
                raise Exception("Slot type not found in env: `{}`".format(slotType))
            slot.type = self.env.slotNamed(slotType)
        else:
            slot.type = self.env.slotNamed('_Generic')
        return slot

    def slex(self, args):
        assert(1 == len(args))
        assert(isinstance(args[0], M.Slex))
        return args[0]

    def slex_call(self, args):
        assert(2 == len(args))
        assert(isinstance(args[0], M.Slot))
        assert(isinstance(args[0].data, M.Slop)) # this might be too strong for runtime-evaluated ops, TBD
        return M.Slex(op = args[0], args = args[1])

    def slex_op(self, args):
        assert(1 == len(args))
        op = args[0]
        if isinstance(op, M.SlotRef):
            op = op.slot
            assert(op) # elsewise NYI
        assert(isinstance(op, M.Slot))
        if not isinstance(op.data, M.Slop):
            raise Exception("Attempt to execute on non-operation: `{}`".format(op.data))
        return op

    def slex_args(self, args):
        return args

    def slot(self, args):
        assert(1 == len(args))
        slot = args[0]
        assert(isinstance(args[0], M.Slot) or isinstance(args[0], M.SlotRef))
        return args[0]

    def slot_name(self, args):
        assert(1 == len(args))
        return args[0].value

    def slot_ref(self, args):
        assert(1 == len(args))
        ref = M.SlotRef(name = args[0].value)
        if self.env.hasSlotNamed(ref.name):
            ref.slot = self.env.slotNamed(ref.name)
        return ref

    def constant(self, args):
        assert(1 == len(args))
        assert(isinstance(args[0], M.Slot))
        return args[0]

    def slop(self, args):
        params = args[0]
        slop = M.Slop()
        locals = args[1] if 3 == len(args) else []
        slotType = self.env.slotNamed('_Slot')
        def _metaSlot(s):
            return M.Slot(type = slotType, data = s, human = M.Human(name = "Meta-{}".format(s.human.name)))
        slop.params = [ _metaSlot(p) for p in params ]
        slop.locals = [ _metaSlot(l) for l in locals ]
        slop.steps = args[-1]
        for x in slop.params + slop.locals:
            assert(x.human.name)
        return M.Slot(type = self.env.slotNamed('_Slop'), data = slop)

    def slop_params(self, args):
        for arg in args:
            assert(arg.human.name)
        return args

    def slop_locals(self, args):
        for arg in args:
            assert(arg.human.name)
        return args

    def slop_steps(self, args):
        return args

    def _token_dispatch(self, tokenClass, token):
        return getattr(self, "_{}_{}".format(tokenClass, token.type))(token.value)
        
    def literal(self, args):
        assert(1 == len(args))
        return self._token_dispatch("literal", args[0])

    def _literal_INTEGER(self, val):
        return M.Slot(type = self.env.slotNamed('_Integer'),
                      data = int(val))


    # TODO / TAI
    def up(self, args):
        assert(1 == len(args))
        return NYI

    def down(self, args):
        assert(1 == len(args))
        NYI
        return 

    # syntactic shortcuts (non-core stuff) follows

    syntactic_shortcut = _simple

    def assignment(self, args):
        assert(2 == len(args))
        assert(isinstance(args[0], M.SlotRef) or isinstance(args[0], M.Slot))
        assert(isinstance(args[1], M.SlotRef) or isinstance(args[1], M.Slot))
        return M.Slex(op = self.env.slotNamed("_Slot_copy"), args = args)


g_commandAliases = {
    "repr" : "r",
    "exec" : "e",
    "structure" : "s",
    "tree" : "t",
}

class CommandMaker(StructureMaker):

    def _simple(self, args):
        assert(1 == len(args))
        return args[0]
    
    cli = _simple
    command_key = _simple

    def command(self, args):
        cmdKey = args[0].value
        cmd = M.Command(key = g_commandAliases.get(cmdKey, cmdKey))
        if len(args) > 1:
            cmd.data = args[1]
        return cmd


# builtin impls:
#   - arg 1 is a dict { name : M.Value }
#   - arg 2 is the parent environment (used for _set)

def _plus(valueDict, parentEnv):
    s = 0
    for x in [ "a", "b", "c", "d" ]: # poor-man's for now
        if x in valueDict:
            s += valueDict[x].impl
    return s

def _set(valueDict, parentEnv):
    atomHandle = _getUsingAliases(valueDict, "name", "n", "key", "k")
    val = _getUsingAliases(valueDict, "value", "v")
    assert(isinstance(atomHandle, M.Value) and isinstance(val, M.Value))
    if (not atomHandle.impl) or (not isinstance(atomHandle.impl, M.Handle)):
        raise Exception("Cannot set value of non-handle {}".format(atomHandle))
    handle = atomHandle.impl
    if (not isinstance(handle.impl, M.Expr)) or (not handle.impl.atom):
        raise Exception("Cannot set value of non-atom-handle {}".format(handle))
    assert(handle.impl.atom and isinstance(handle.impl.atom, str))
    parentEnv[handle.impl.atom] = val
    return val.impl


# impl helpers

def _getUsingAliases(valueDict, *args):
    for arg in args:
        if arg in valueDict:
            return valueDict[arg]
    return None
    
