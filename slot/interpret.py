
from . import model as M
from .builtin import builtinContext
from .link import Linker
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
        self._linker = Linker()
        self._instantiator = Instantiator()
        self._executor = Executor(self)
        self._context = builtinContext().derive()
        self.raiseOnError = False


    def reset(self):
        self._context = builtinContext().derive()


    @property
    def parser(self):
        return self._parser

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


    @property
    def definer(self):
        return self._definer
        
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


    @property
    def linker(self):
        return self._linker

    def link(self, parsed):
        if not parsed:
            return None
        elif isinstance(parsed, list):
            return [ self._link(x) for x in parsed ]
        else:
            return self._link(parsed)

    def _link(self, parsed):
        if not parsed:
            return None
        if not Linker.canLink(parsed):
            self.error("Cannot link: {}".format(displayStructure(parsed)))
            return None
        try:
            return self._linker.link(parsed, self._context)
        except Exception as e:
            self.error("Compilation failed: {}".format(e))
            if self.raiseOnError:
                raise e
            return None


    @property
    def instantiator(self):
        return self._instantiator

    def instantiate(self, linked):
        if not linked:
            return None
        elif isinstance(linked, list):
            return [ self._instantiate(x) for x in linked ]
        else:
            return self._instantiate(linked)

    def _instantiate(self, linked):
        if not linked:
            return None
        if not Instantiator.canInstantiate(linked):
            self.error("Cannot instantiate: {}".format(displayStructure(linked)))
            return None
        try:
            return self._instantiator.instantiate(linked)
        except Exception as e:
            self.error("Instantiation failed: {}".format(e))
            if self.raiseOnError:
                raise e
            return None


    @property
    def executor(self):
        return self._executor

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
            return self.execute(self.instantiate(self.link(defined)))
        elif defined.fsType == fs.SlotDef:
            return self.instantiate(self.link(defined))
        elif defined.fsType == fs.SlotRef:
            return self._instantiator.instantiatedSlot(self.link(defined))
        elif defined.fsType == fs.SlopDef:
            return self.link(defined)
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
