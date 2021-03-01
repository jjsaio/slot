
from . import model as M
from .builtin import builtinNamespace
from .define import Definer
from .display import displayStructure
from .execute import Executor
from .instantiate import Instantiator
from .link import Linker
from .logging import LoggingClass
from .parse import Parser, ParseTree
from .util import strWithFileAtPath


class Interpreter(LoggingClass):

    def __init__(self, parseMode = "interpreter", allowShortcuts = True):
        LoggingClass.__init__(self)
        #self.setLevelDebug()
        self._parser = Parser(mode = parseMode, shortcuts = allowShortcuts)
        self._definer = Definer()
        self._linker = Linker()
        self._instantiator = Instantiator()
        self._executor = Executor(self)
        self._namespace = builtinNamespace().derive()

    @property
    def namespace(self):
        return self._namespace

    def reset(self):
        self._namespace = builtinNamespace().derive()


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
            raise Exception("Syntax error: {}".format(e))


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
            raise Exception("Definition failed: {}".format(e))


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
            raise Exception("Cannot link: {}".format(displayStructure(parsed)))
        try:
            return self._linker.link(parsed, self._namespace)
        except Exception as e:
            raise Exception("Linking failed: {}".format(e))


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
            raise Exception("Cannot instantiate: {}".format(displayStructure(linked)))
        try:
            return self._instantiator.instantiate(linked)
        except Exception as e:
            raise Exception("Instantiation failed: {}".format(e))

    def instantiatedSlot(self, mslot):
        return self._instantiator.instantiatedSlot(mslot)


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
                raise Exception("Cannot execute: {}".format(displayStructure(inst)))
            self._executor.execute(inst)
            return True
        except Exception as e:
            raise Exception("Execution failed: {}".format(e))


    def run(self, path):
        script = strWithFileAtPath(path)
        slop = self.link(self.define(self.parse(script)))
        self.execute(M.Slex(op = slop))
