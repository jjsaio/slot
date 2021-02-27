
import os

from . import model as M
from .builtin import builtinContext
from .compile import Compiler
from .display import displayStructure
from .execute import Executor
from .instantiate import Instantiator
from .logging import LoggingClass
from .parse import Parser
from .util import prettyJson, strWithFileAtPath


class Interactive(LoggingClass):

    def __init__(self):
        LoggingClass.__init__(self, initLogging = True, loggingFormat = LoggingClass.noStampFormat)
        #self.setLevelDebug()
        self._parser = Parser(mode = "interactive")
        self._compiler = Compiler()
        self._instantiator = Instantiator()
        self._executor = Executor()
        self._context = builtinContext().derive()
        self._raiseOnError = False
        self._showJson = False
        self._setup()
        if True:
            self.mode = "p"
            self._raiseOnError = True

    def _parse(self, theStr):
        assert(isinstance(theStr, str))
        try:
            parseResult = self._parser.parse(theStr)
        except Exception as e:
            self.error("Syntax error: {}".format(e))
            if self._raiseOnError:
                raise e
            return None
        try:
            parsed = parseResult.definition()
        except Exception as e:
            self.error("Transform error: {}".format(e))
            if self._raiseOnError:
                raise e
            return None
        return parsed

    def _compile(self, parsed):
        if not parsed:
            return None
        if not Compiler.canCompile(parsed):
            self.error("Cannot compile: {}".format(displayStructure(parsed)))
            return None
        try:
            compiled = self._compiler.compile(parsed, self._context)
        except Exception as e:
            self.error("Compilation error: {}".format(e))
            if self._raiseOnError:
                raise e
            return None
        return compiled

    def _instantiate(self, compiled):
        if not compiled:
            return None
        if not Instantiator.canInstantiate(compiled):
            self.error("Cannot instantiate: {}".format(displayStructure(compiled)))
            return None
        try:
            inst = self._instantiator.instantiate(compiled)
        except Exception as e:
            self.error("Instantiation error: {}".format(e))
            if self._raiseOnError:
                raise e
            return None
        return inst

    def _exec(self, inst):
        if not inst:
            return False
        assert(isinstance(inst, list))
        try:
            for slex in inst:
                if not Executor.canExecute(slex):
                    self.error("Cannot execute: {}".format(displayStructure(slex)))
                    return False
                self._executor.execute(slex)
        except Exception as e:
            self.error("Execution error: {}".format(e))
            if self._raiseOnError:
                raise e
            return False
        return True

    def _setup(self):
        self.modes = {
            "d" : [ "desig", "designation", "default", "normal" ],
            "p" : [ "parse", "tree", "parseTree" ],
            "t" : [ "tree", "parseTree" ],
            "c" : [ "compile" ],
            "i" : [ "inst", "instantiate" ],
            "e" : [ "exec", "execute" ],
        }
        self.commands = {
            "h" : [ "help" ],
            "w" : [ "wipe", "reset" ],
            "v" : [ "env", "environment", "ctx", "context" ],
            "b" : [ "batch" ],
            "g" : [ "debug" ],
            "k" : [ "kernel" ],
            "j" : [ "json" ],
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

    def go(self):
        self.running = True
        aliasMap = {}
        for k, v in list(self.modes.items()) + list(self.commands.items()):
            aliasMap[k] = k
            for a in v:
                aliasMap[a] = k
        self.mode = self.mode or aliasMap["designation"]

        while self.running:
            try:
                resp = input(">{}> ".format(self.mode))
            except:
                self._cmd_q() # Ctrl-C, Ctlr-D
                return
            if not resp:
                continue
            elif resp[0] == '.':
                self._doCommand(resp[1:])
            else:
                self._dispatch(self.mode, resp)


    def _cmd_t(self, resp):
        try:
            parseResult = self._parser.parse(resp)
            parseResult.visualizeTree(show = True)
        except Exception as e:
            self.error("Syntax error: {}".format(e))
            if self._raiseOnError:
                raise e

    def _showResult(self, struc):
        if not struc:
            return
        if isinstance(struc, list):
            for s in struc:
                self._showResult(s)
        elif self._showJson:
            print(prettyJson(struc.json()))
        else:
            print(" " + displayStructure(struc))

    def _cmd_p(self, resp):
        self._showResult(self._parse(resp))

    def _cmd_c(self, resp):
        self._showResult(self._compile(self._parse(resp)))

    def _cmd_i(self, resp):
        self._showResult(self._instantiate(self._compile(self._parse(resp))))

    def _cmd_e(self, resp):
        if self._exec(self._instantiate(self._compile(self._parse(resp)))):
            print(" OK")

    def _cmd_d(self, resp):
        compiled = self._compile(self._parse(resp))
        NYI
        if isinstance(struc, M.Slot):
            print(" " + displayStructure(struc.data))
        else:
            self.warn("Designation undefined for `{}`".format(struc))


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
        self._hasError = False
        for line in batch:
            if self._hasError:
                break
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
                self._dispatch(cmd, rest)
            else:
                self.error("Invalid command/mode `{}` in batch, aborting.".format(cmd))
        self.info("batch done")

    def _cmd_w(self, struc):
        self._context = Context()
        self.info("context wiped")

    def _cmd_v(self, rest):
        print(self._context.dump(all = (rest and (rest[0] == "a"))))

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

    def _cmd_k(self, _):
        if self._parser.shortcuts:
            self._parser = Parser(mode = "interactive", shortcuts = False)
            self.info("kernel mode parsing (no syntactic shortcuts)")
        else:
            self._parser = Parser(mode = "interactive", shortcuts = True)
            self.info("general parsing (shortcuts allowed")

    def _cmd_j(self, _):
        self._showJson = not self._showJson
        if self._showJson:
            self.info("JSON display")
        else:
            self.info("standard display")

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
