
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
        cur = slex
        while cur:
            self._executeSlex(cur)
            cur = cur.next

    def _executeSlex(self, slex):
        assert(isinstance(slex, M.Slex))
        self.debug("execSlex:", slex)

        # get the op
        slop = slex.op
        if (not slop) or (not isinstance(slop, M.Slop)):
            raise Exception("Cannot execute Slex with non-Slop op: {}".format(slop))

        # native handling can just pass the args directly
        if slop.native:
            self.debug("native", slex)
            slop.native(slex, self)
            return

        # instantiate the parameters (using the args)
        inst = self._instantiator
        assert(len(slex.args) == len(slop.params))
        for param, arg in zip(slop.params, slex.args):
            inst.instantiateMetaSlot(param, arg)

        # instantiate the locals
        for loc in slop.locals:
            inst.instantiateMetaSlot(loc)

        # instantiate the slexes, set up continuations
        self.debug("instantiate drop steps:", slop.steps)
        myNext = slex.next
        cur = slex
        for ms in slop.steps:
            cur.next = inst.instantiateMetaSlex(ms)
            cur = cur.next
        cur.next = myNext

        # uninstantiate the MetaSlots we instantiated
        # important that this is *before* exec, in order to support recursion (re-use of MetaSlots)
        #  (we'd probably have to hold a lock (at the slop object) in a multi-threaded env)
        for ms in slop.params + slop.locals:
            inst.uninstantiateMetaSlot(ms)

        # continuation is set up and will be next executed
        self.debug("exec done, coming up:", slex.next)
