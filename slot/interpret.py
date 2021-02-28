
from . import model as M
from .builtin import builtinContext
from .compile import Compiler
from .define import Definer
from .display import displayStructure
from .execute import Executor
from .fs import fs
from .instantiate import Instantiator
from .logging import LoggingClass
from .parse import Parser, ParseTree


class Interpreter(LoggingClass):

    def __init__(self, parseMode = "interpreter", allowShortcuts = True):
        LoggingClass.__init__(self)
        #self.setLevelDebug()
        self._parser = Parser(mode = parseMode, shortcuts = allowShortcuts)
        self._definer = Definer()
        self._compiler = Compiler()
        self._instantiator = Instantiator()
        self._executor = Executor(self._instantiator)
        self._context = builtinContext().derive()
        self.raiseOnError = False

    def reset(self):
        self._context = builtinContext().derive()

    @property
    def allowShortcuts(self):
        return self._parser.shortcuts

    @allowShortcuts.setter
    def allowShortcuts(self, allow):
        self._parser = Parser(mode = self._parser.mode, shortcuts = allow)
        if self._parser.shortcuts:
            self.debug("general parsing (shortcuts allowed)")
        else:
            self.debug("kernel mode parsing (no syntactic shortcuts)")

    def parse(self, theStr):
        assert(isinstance(theStr, str))
        try:
            return self._parser.parse(theStr)
        except Exception as e:
            self.error("Syntax error: {}".format(e))
            if self.raiseOnError:
                raise e
            return None
        
    def define(self, tree):
        if not tree:
            return None
        assert(isinstance(tree, ParseTree))
        try:
            return self._definer.define(tree)
        except Exception as e:
            self.error("Definition failed: {}".format(e))
            if self.raiseOnError:
                raise e
            return None

    def compile(self, parsed):
        if not parsed:
            return None
        elif isinstance(parsed, list):
            return [ self._compile(x) for x in parsed ]
        else:
            return self._compile(parsed)

    def _compile(self, parsed):
        if not parsed:
            return None
        if not Compiler.canCompile(parsed):
            self.error("Cannot compile: {}".format(displayStructure(parsed)))
            return None
        try:
            return self._compiler.compile(parsed, self._context)
        except Exception as e:
            self.error("Compilation failed: {}".format(e))
            if self.raiseOnError:
                raise e
            return None

    def instantiate(self, compiled):
        if not compiled:
            return None
        elif isinstance(compiled, list):
            return [ self._instantiate(x) for x in compiled ]
        else:
            return self._instantiate(compiled)

    def _instantiate(self, compiled):
        if not compiled:
            return None
        if not Instantiator.canInstantiate(compiled):
            self.error("Cannot instantiate: {}".format(displayStructure(compiled)))
            return None
        try:
            return self._instantiator.instantiate(compiled)
        except Exception as e:
            self.error("Instantiation failed: {}".format(e))
            if self.raiseOnError:
                raise e
            return None

    def execute(self, inst):
        if not inst:
            self.warn("Nothing to execute")
            return False
        elif isinstance(inst, list):
            for i in inst:
                if not self._execute(i):
                    return False
            return True
        else:
            return self._execute(inst)

    def _execute(self, inst):
        if not inst:
            return False
        try:
            if not Executor.canExecute(inst):
                self.error("Cannot execute: {}".format(displayStructure(slex)))
                return False
            self._executor.execute(inst)
            return True
        except Exception as e:
            self.error("Execution failed: {}".format(e))
            if self.raiseOnError:
                raise e
            return False

    def handleDefinition(self, defined):
        if defined.fsType == fs.SlexDef:
            return self.execute(self.instantiate(self.compile(defined)))
        elif defined.fsType == fs.SlotDef:
            return self.instantiate(self.compile(defined))
        elif defined.fsType == fs.SlotRef:
            return self._instantiator.instantiatedSlot(self.compile(defined))
        elif defined.fsType == fs.SlopDef:
            return self.compile(defined)
        else:
            self.error("Unhandled definition type `{}`".format(defined))
            return False

    def handle(self, inputString):
        assert(isinstance(inputString, str))
        _raiseOnError = self.raiseOnError
        self.raiseOnError = True
        try:
            last = None
            for defined in (self.define(self.parse(inputString)) or []):
                res = self.handleDefinition(defined)
                if not res:
                    break
                if (not last) or (res != True):
                    last = res
            return last
        except Exception as e:
            if _raiseOnError:
                raise e
            return None
        finally:
            self.raiseOnError = _raiseOnError
