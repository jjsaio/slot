
import os

from .fs import fs
from .logging import LoggingClass
from .util import prettyJson, strWithFileAtPath

from . import model as M

def slot_displayType(x):
    return (x.human.displayType or "??") if (x and x.human) else "??"

def slot_repr(x):
    t = type(x).__name__
    if isinstance(x, M.Slot) or isinstance(x, M.MetaSlot):
        d = slot_displayType(x.type)
    elif isinstance(x, M.Slop):
        d = "..." # TBD
    elif isinstance(x, M.Slex):
        d = "..."  # TBD
    elif callable(x):
        d = impl.__name__
    elif hasattr(x, 'json'):
        d = x.json()
        d = str(d)
        if len(d) > 32:
            d = d[:28] + "...}"
    else:
        d = repr(x)
    return "<{}:{}>".format(t, d)

def _Integer_plus(slex):
    slop = slex.op
    # these asserts should be done by _execute, just doing here for illustration
    if False:
        assert(_Integer_plus == slop.native)
        assert(3 == len(slex.args))
        for i in range(len(slop.params)):
            assert(slop.params[i].type == slex.args[i].type)
    slex.args[0].data = slex.args[1].data + slex.args[2].data

def _Slot_copy(slex):
    slex.args[0].data = slex.args[1].data

    
class Environment(object):

    def __init__(self, parent = None):
        self._parent = parent
        self._namedSlots = {}
        self._anonymousSlots = []
        self._setupRuntime()

    def _setupRuntime(self):
        generic = self.addNamedSlot('_Generic', M.Slot(human = M.Human(name = "Generic (untyped) slot", displayType = "*")))

        nat = self.addNamedSlot('_Native', M.Slot(human = M.Human(name = "Generic type for Native (scalar) types", displayType = "scalar")))
        integer = self.addNamedSlot('_Integer', M.Slot(type = nat, data = fs.Integer, human = M.Human(name = "Native Integer type", displayType = "Integer")))

        self.addNamedSlot('_Slot', M.Slot(type = nat, data = fs.Slot, human = M.Human(displayType = "Slot")))
        slop = self.addNamedSlot('_Slop', M.Slot(type = nat, data = fs.Slop, human = M.Human(displayType = "Slop")))
        self.addNamedSlot('_Slex', M.Slot(type = nat, data = fs.Slex, human = M.Human(displayType = "Slex")))

        self.addBuiltin("plus", _Integer_plus,
                        params = [ M.Slot(type = integer), M.Slot(type = integer), M.Slot(type = integer) ])
        self.addBuiltin("_Slot_copy", _Slot_copy,
                        params = [ M.Slot(type = generic), M.Slot(type = generic) ])

    def dump(self, all = False):
        lines = [ "Environment @ {}".format(id(self)) ]
        for name in sorted(self._namedSlots.keys()):
            if (not all) and name.startswith('_'):
                continue
            s = self._namedSlots[name]
            if isinstance(s, M.Slot):
                lines.append("  {} -> {} => {}".format(name, slot_repr(s), slot_repr(s.data)))
            else:
                lines.append("  {} -> {}".format(name, slot_repr(s)))
        for slot in self._anonymousSlots:
            if isinstance(s, M.Slot):
                lines.append("  ANON  {} => {}".format(slot_repr(slot), slot_repr(slot.data)))
            else:
                lines.append("  ANON  {}".format(slot_repr(s)))
        return "\n".join(lines)

    def addBuiltin(self, name, handler, params):
        self.addNamedSlot(name, M.Slot(type = self._namedSlots['_Slop'],
                                       data = M.Slop(params = params,
                                                     native = handler)))

    def derive(self):
        return Environment(self)

    def hasSlotNamed(self, n):
        return (n in self._namedSlots) or (self._parent and self._parent.hasSlotNamed(n))

    def slotNamed(self, n):
        return self._namedSlots.get(n, self._parent.slotNamed(n) if self._parent else None)

    def addNamedSlot(self, name, slot):
        if name in self._namedSlots:
            raise Exception("Slot already exists in environment: `{}`".format(name))
        self._namedSlots[name] = slot
        return slot

    def addSlot(self, slot):
        self._anonymousSlots.append(slot)
        return slot


class Slot(LoggingClass):

    def __init__(self):
        LoggingClass.__init__(self, initLogging = True, loggingFormat = LoggingClass.noStampFormat)
        #self.setLevelDebug()
        self._parser = None
        self._raiseOnError = False
        self._env = Environment()
        self._setup()

    @property
    def parser(self):
        if not self._parser:
            from .grammar import Parser
            self._parser = Parser()
        return self._parser

    def _exec(self, slex):
        # TODO: need to be careful about the weeds & the vortex
        # exec takes HANDLES to Slex, not slex...
        if not isinstance(slex, M.Slex):
            return False

        self.debug("_exec", prettyJson(slex.json()))

        assert(isinstance(slex.op, M.Slot))
        slop = slex.op.data
        assert(isinstance(slop, M.Slop))
        for arg in slex.args:
            assert(isinstance(arg, M.Slot))

        # natives: just exec, given the passed-in slots 
        self.debug("_exec:", slop.human.name if slop.human else slop.native, slex.args)
        if slop.native:
            assert(not slop.locals)
            slop.native(slex)
            return True

        # ok, we need to instantiate the MetaSlots/MetaSlexes into Slots/Slexes

        # first, set up the args/parameters:
        assert(len(slex.args) == len(slop.params))
        for arg, param in zip(slex.args, slop.params):
            # set the metaslot to the passed-in arg
            assert(not param.instanced)
            # TODO: verify here that arg.type is compatible with orig.type 
            # the passed-in slot is to be used in this execution context
            param.instanced = arg

        # create new slot instances for the locals
        for loc in slop.locals:
            assert(not loc.instanced)
            loc.instanced = M.Slot(type = loc.type, human = loc.human)

        # define "drop" for (Slot or MetaSlot) to a Slot
        def _drop(s):
            if isinstance(s, M.Slot):
                return s
            assert(isinstance(s, M.MetaSlot))
            if s.instanced:
                return s.instanced # note this allows instanced to take precedence over concrete, e.g., a name was re-bound locally
            assert(s.concrete)
            return s.concrete

        # now create all of the metaslexes; it's important to do this
        # before execution, otherwise this will fail if a slop is
        # called recursively
        self.debug("_exec drop steps:", slop.steps)
        dropped = []
        for step in slop.steps:
            dropped.append(M.Slex(op = _drop(step.op),
                                  args = [ _drop(a) for a in step.args ],
                                  human = step.human))

        # clear the instanced slots, since they're all set up in the
        # dropped ones now
        for ms in slop.params + slop.locals:
            ms.instanced = None

        # finally, we can exec the dropped slexes
        for step in dropped:
            self.debug("_exec subexec:", step)
            self._exec(step)
            
        return True

    def _parse(self, theStr):
        assert(isinstance(theStr, str))
        try:
            parseResult = self.parser.parse(theStr)
        except Exception as e:
            self.error("Syntax error: {}".format(e))
            if self._raiseOnError:
                raise e
            return None
        if self.mode == 'p':
            return parseResult
        try:
            return parseResult.structure(self._env)
        except Exception as e:
            self.error("Transform error: {}".format(e))
            if self._raiseOnError:
                raise e
            return None

    def _setup(self):
        self.modes = {
            "d" : [ "desig", "designation" ],
            "e" : [ "exec", "execution" ],
            "s" : [ "struc", "structure" ],
            "p" : [ "parse", "tree", "parseTree" ],
        }
        self.commands = {
            "h" : [ "help" ],
            "w" : [ "wipe", "reset" ],
            "v" : [ "env", "environment" ],
            "b" : [ "batch" ],
            "g" : [ "debug" ],
            "x" : [ "raise", "raiseOnError", "except", "exception" ],
            "q" : [ "quit", "exit" ],
        }

    def _doCommand(self, resp):
        bits = resp.split(' ')
        cmd = bits[0]
        if cmd in self.modes:
            self.mode = cmd
        elif cmd in self.commands:
            self._dispatch(cmd, ' '.join(bits[1:]))
        else:
            self.error("Invalid command/mode:", cmd)

    def _dispatch(self, cmd, arg):
        getattr(self, "_cmd_{}".format(cmd))(arg)

    def interactive(self):
        self.running = True
        aliasMap = {}
        for k, v in list(self.modes.items()) + list(self.commands.items()):
            aliasMap[k] = k
            for a in v:
                aliasMap[a] = k
        self.mode = aliasMap["structure"]

        while self.running:

            try:
                resp = input(">{}> ".format(self.mode))
            except:
                # Ctrl-C
                self._cmd_q()
                return

            if not resp:
                continue
            if resp[0] == '.':
                self._doCommand(resp[1:])
                continue

            struc = self._parse(resp)
            if struc:
                self._dispatch(self.mode, struc)

    def _cmd_b(self, resp):
        if not os.path.exists(resp):
            resp += ".batch"
        if not os.path.exists(resp):
            resp = os.path.join('misc', resp)
        try:
            batch = strWithFileAtPath(resp).split('\n')
        except Exception as e:
            self.error("Opening batch: ", e)
            return
        self.info("batch start: ", resp)
        for line in batch:
            cmd, rest = line[:1], line[1:].strip()
            if (not cmd) or (cmd == '#'):
                continue
            if (not self.running) or cmd == 'f':
                # f is shorthand for "finish this batch"
                break
            print(">{}> {}".format(cmd, rest))
            if cmd in self.commands:
                self._doCommand(line)
            elif cmd in self.modes:
                struc = self._parse(rest)
                self._dispatch(cmd, struc)
            else:
                self.error("Invalid command/mode `{}` in batch, aborting.".format(cmd))
                break
        self.info("batch done")

    def _cmd_s(self, struc):
        print(" " + slot_repr(struc))

    def _cmd_d(self, struc):
        if isinstance(struc, M.Slot):
            print(" " + slot_repr(struc.data))
        else:
            self.warn("Designation undefined for `{}`".format(struc))

    def _cmd_e(self, struc):
        if self._exec(struc):
            print(" OK")
        else:
            self.warn("Cannot execute: `{}`".format(slot_repr(struc)))

    def _cmd_p(self, parseResult):
        parseResult.visualizeTree(show = True)

    def _cmd_w(self, struc):
        self._env = Environment()
        self.info("environment wiped")

    def _cmd_v(self, rest):
        print(self._env.dump(all = (rest and (rest[0] == "a"))))

    def _cmd_x(self, rest):
        self._raiseOnError = not self._raiseOnError
        self.info("{}raising exceptions on error".format("" if self._raiseOnError else "not " ))

    def _cmd_g(self, _):
        if self.isLevelDebug():
            self.setLevelInfo()
            self.info("debug level off")
        else:
            self.setLevelDebug()
            self.debug("debug level set")

    def _cmd_h(self, _):
        print("Modes:")
        for key in sorted(self.modes.keys()):
            print("  {}: {}".format(key, ", ".join(self.modes[key])))
        print("Commands:")
        for key in sorted(self.commands.keys()):
            print("  {}: {}".format(key, ", ".join(self.commands[key])))
            
    def _cmd_q(self, _ = None):
        self.running = False
        print("Bye!")
