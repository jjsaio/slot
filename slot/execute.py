
from . import model as M
from .logging import LoggingClass


class Executor(LoggingClass):

    def __init__(self, instantiator):
        LoggingClass.__init__(self)
        self._instantiator = instantiator
        #self.setLevelDebug()

    def canExecute(obj):
        return obj and isinstance(obj, M.Slex)

    def execute(self, slex):
        self.executeSlex(slex)

    def executeSlex(self, slex):
        assert(isinstance(slex, M.Slex))

        # get the op
        slop = slex.op.data
        if (not slop) or (not isinstance(slop, M.Slop)):
            raise Exception("Cannot execute Slex with non-Slop op: {}".format(slop))

        # native handling can just pass the args directly
        if slop.native:
            slop.native(slex)
            return

        # instantiate the parameters (using the args)
        inst = self._instantiator
        assert(len(slex.args) == len(slop.params))
        for param, arg in zip(slop.params, slex.args):
            inst.instantiateMetaSlot(param, arg)

        # instantiate the locals
        for loc in slop.locals:
            inst.instantiateMetaSlot(loc)

        # instantiate the slexes
        self.debug("instantiate drop steps:", slop.steps)
        executables = [ inst.instantiateMetaSlex(ms) for ms in slop.steps ]

        # uninstantiate the MetaSlots we instantiated
        # important that this is *before* exec, in order to support recursion (re-use of MetaSlots)
        #  (we'd probably have to hold a lock (at the slop object) in a multi-threaded env)
        for ms in slop.params + slop.locals:
            inst.uninstantiate(ms)

        # and execute
        for slex in instantiated:
            self.executeSlex(slex)
