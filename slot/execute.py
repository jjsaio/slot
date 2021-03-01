
from . import model as M
from .logging import LoggingClass


class Executor(LoggingClass):

    def __init__(self, interpreter):
        LoggingClass.__init__(self)
        self._execContext = M.ExecutionContext(interpreter = interpreter)
        #self.setLevelDebug()

    def canExecute(obj):
        return obj and isinstance(obj, M.Slex)

    def execute(self, slex):
        self.executeSlex(slex)

    def executeSlex(self, slex):
        assert(isinstance(slex, M.Slex))
        cur = M.ExecutionNode(slex = slex)
        if self._execContext.node:
            cur.next = self._execContext.node.next
            self._execContext.node.next = cur
            return
        while cur:
            self._execContext.node = cur
            self._executeNode(cur)
            cur.executed = True
            cur = cur.next
        self._execContext.node = None

    def _executeNode(self, exNode):
        slex = exNode.slex
        assert(isinstance(slex, M.Slex))
        assert(not exNode.executed)
        ctx = self._execContext
        ctx.node = exNode
        self.debug("execSlex:", slex)

        # get the op
        slop = slex.op
        if (not slop) or (not isinstance(slop, M.Slop)):
            raise Exception("Cannot execute Slex with non-Slop op: {}".format(slop))

        # native handling can just pass the args directly
        if slop.native:
            self.debug("native", slex)
            slop.native(ctx)
            return

        # instantiate the parameters (using the args)
        inst = ctx.interpreter.instantiator
        assert(len(slex.args) == len(slop.params))
        for param, arg in zip(slop.params, slex.args):
            self.debug("INSTp", param)
            inst.instantiateMetaSlot(param, arg)

        # instantiate the locals
        for loc in slop.locals:
            if not loc.concrete:
                self.debug("INSTl", loc)
                inst.instantiateMetaSlot(loc)

        # instantiate the slexes, set up continuations
        myNext = exNode.next
        cur = exNode
        for ms in slop.steps:
            step = M.ExecutionNode(slex = inst.instantiateMetaSlex(ms))
            step.parent = exNode
            cur.next = step
            cur = cur.next
        cur.next = myNext

        # uninstantiate the MetaSlots we instantiated
        # important that this is *before* the steps execute, in order to support recursion (re-use of MetaSlots)
        #  (this is not an in issue for a singleton, serialized, tail-recursive executor)
        #  (in multi-executor environment, we'd probably have to hold a lock at the slop object)
        for ms in slop.params + slop.locals:
            if not ms.concrete:
                self.debug("unINST", ms)
                inst.uninstantiateMetaSlot(ms)

        # continuation is set up and will be next executed
        self.debug("exec done, coming up:", exNode.next)
