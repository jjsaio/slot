
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
        assert(struc.fsType in [ fs.Slot, fs.SlotRef, fs.Slex, fs.Slop, fs.MetaSlot, fs.MetaSlex ])
        self.debug("_fixRefs", struc)
        return getattr(self, "_fixRefs_{}".format(fs.toString(struc.fsType)))(struc, env)

    def _fixRefs_Slot(self, slot, env):
        assert(isinstance(slot, M.Slot))
        if slot.data and hasattr(slot.data, 'fsType') and (slot.data.fsType in [ fs.Slot, fs.SlotRef, fs.Slex, fs.Slop ]):
            slot.data = self._fixRefs(slot.data, env)
        return slot

    def _fixRefs_MetaSlot(self, slot, env):
        assert(isinstance(slot, M.MetaSlot))
        assert(not slot.instanced)
        if slot.concrete:
            slot.concrete = self._fixRefs(slot.concrete, env)
        return slot

    def _fixRefs_SlotRef(self, ref, env):
        if not env.hasSlotNamed(ref.name):
            raise Exception("Unbound slot reference: `{}`".format(ref.name))
        return env.slotNamed(ref.name)

    def _fixRefs_Slex(self, slex, env):
        assert(isinstance(slex, M.Slex))
        slex.op = self._fixRefs(slex.op, env)
        slex.args = [ self._fixRefs(x, env) for x in slex.args ]
        return slex

    def _fixRefs_MetaSlex(self, slex, env):
        assert(isinstance(slex, M.MetaSlex))
        slex.op = self._fixRefs(slex.op, env)
        slex.args = [ self._fixRefs(x, env) for x in slex.args ]
        return slex

    def _fixRefs_Slop(self, slop, env):
        assert(isinstance(slop, M.Slop))
        slopEnv = env.derive()
        for param in slop.params:
            assert(isinstance(param, M.MetaSlot))
            if param.human and param.human.name:
                slopEnv.addNamedSlot(param.human.name, param)
            else:
                # builtins may not have named slots
                slopEnv.addSlot(param)
        for local in slop.locals:
            assert(isinstance(local, M.MetaSlot))
            slopEnv.addNamedSlot(local.human.name, local)
        self.debug("slop derived env:", slopEnv.dump())
        for step in slop.steps:
            self._fixRefs_MetaSlex(step, slopEnv)
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

    def _slotType(self, arg):
        if not arg:
            return self.env.slotNamed('_Generic')
        slotType = {
            "Integer" : "_Integer",
            "int" : "_Integer",
            "String" : "_String",
            "str" : "_String",
        }.get(arg, arg)
        if not self.env.hasSlotNamed(slotType):
            raise Exception("Slot type not found in env: `{}`".format(slotType))
        return self.env.slotNamed(slotType)

    def slot_spec(self, args):
        assert(len(args) >= 1  and  len(args) <= 3)
        assert(len(args) < 3) # slot ctor TBD
        return M.Slot(type = self._slotType(args[1] if len(args) > 1 else None), human = M.Human(name = args[0]))

    def metaslot_spec(self, args):
        assert(len(args) >= 1  and  len(args) <= 3)
        assert(len(args) < 3) # slot ctor TBD
        return M.MetaSlot(type = self._slotType(args[1] if len(args) > 1 else None), human = M.Human(name = args[0]))

    def _metaSlot(self, slot):
        if isinstance(slot, M.SlotRef):
            return slot
        assert(isinstance(slot, M.Slot))
        return M.MetaSlot(type = slot.type, concrete = slot, human = slot.human)

    def metaslex(self, args):
        assert(1 == len(args))
        slex = args[0]
        assert(isinstance(slex, M.Slex))
        return M.MetaSlex(op = self._metaSlot(slex.op),
                          args = [ self._metaSlot(s) for s in slex.args ],
                          human = slex.human)

    def slex(self, args):
        assert(1 == len(args))
        assert(isinstance(args[0], M.Slex))
        return args[0]

    def slex_call(self, args):
        assert(2 == len(args))
        assert(isinstance(args[0], M.Slot) or isinstance(args[0], M.SlotRef))
        return M.Slex(op = args[0], args = args[1])

    def slex_op(self, args):
        assert(1 == len(args))
        op = args[0]
        assert(isinstance(op, M.SlotRef)  or  isinstance(op, M.Slot))
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
        return M.SlotRef(name = args[0].value)

    def constant(self, args):
        assert(1 == len(args))
        assert(isinstance(args[0], M.Slot))
        return args[0]

    def slop(self, args):
        slop = M.Slop(params = args[0],
                      locals = args[1] if 3 == len(args) else [],
                      steps = args[-1])
        for s in slop.params + slop.locals:
            assert(isinstance(s, M.MetaSlot) or isinstance(s, M.SlotRef))
            assert(s.human.name)
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
    
