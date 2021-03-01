
from . import model as M
from .display import debugString
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
        self.debug("execSlex:", debugString(slex), " -- ", debugString(slex.op))

        # get the op
        slop = slex.op.op
        if (not slop) or (not isinstance(slop, M.MetaSlop)):
            raise Exception("Cannot execute Slex with non-Slop op: {}".format(slop))

        # native handling can just pass the args directly
        if slop.native:
            self.debug("native", slex)
            slop.native(ctx)
            return

        inst = ctx.interpreter.instantiator
        instantiated = []
        def _addInstantiated(imslot, islot = None):
            res = inst.instantiateMetaSlot(imslot, islot)
            if res == imslot.instanced:
                instantiated.append(imslot)

        # instantiate the captured slots
        assert(len(slex.op.captured) == len(slop.captured))
        for cslot, cap in zip(slop.captured, slex.op.captured):
            if not cslot.instanced:
                self.debug("INSTc", cslot)
                _addInstantiated(cslot, cap)

        # instantiate the parameters (using the args)
        assert(len(slex.args) == len(slop.params))
        for param, arg in zip(slop.params, slex.args):
            self.debug("INSTp", param)
            _addInstantiated(param, arg)

        # instantiate the locals
        for loc in slop.locals:
            self.debug("LOC", debugString(loc))
            _addInstantiated(loc)

        # instantiate the slexes, set up continuations
        myNext = exNode.next
        cur = exNode
        for ms in slop.steps:
            self.debug("inst step: ", debugString(ms), " --- ", debugString(slop))
            step = M.ExecutionNode(slex = inst.instantiateMetaSlex(ms))
            step.parent = exNode
            cur.next = step
            cur = cur.next
        cur.next = myNext

        # uninstantiate the MetaSlots we instantiated
        # important that this is *before* the steps execute, in order to support recursion (re-use of MetaSlots)
        #  (this is not an in issue for a singleton, serialized, tail-recursive executor)
        #  (in multi-executor environment, we'd probably have to hold a lock at the slop object)
        for ms in instantiated:
            self.debug("unINST", debugString(ms))
            inst.uninstantiateMetaSlot(ms)

        # continuation is set up and will be next executed
        self.debug("exec done, coming up:", exNode.next)
