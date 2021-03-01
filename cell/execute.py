
from . import model as M
from .display import debugString
from .logging import LoggingClass


class Executor(LoggingClass):

    def __init__(self, interpreter):
        LoggingClass.__init__(self)
        self._execContext = M.ExecutionContext(interpreter = interpreter)
        #self.setLevelDebug()

    def canExecute(obj):
        return obj and isinstance(obj, M.Do)

    def execute(self, do):
        self.executeDo(do)

    def executeDo(self, do):
        assert(isinstance(do, M.Do))
        cur = M.ExecutionNode(do = do)
        if self._execContext.node:
            cur.parent = self._execContext.node
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
        do = exNode.do
        assert(isinstance(do, M.Do))
        assert(not exNode.executed)
        ctx = self._execContext
        ctx.node = exNode
        self.debug("execDo:", debugString(do), " -- ", debugString(do.op))

        # get the op
        cop = do.op.op
        if (not cop) or (not isinstance(cop, M.MetaCop)):
            raise Exception("Cannot execute Do with non-Cop op: {}".format(cop))

        # native handling can just pass the args directly
        if cop.native:
            self.debug("native", do)
            cop.native(ctx)
            return

        inst = ctx.interpreter.instantiator
        instantiated = []
        def _addInstantiated(imcell, icell = None):
            res = inst.instantiateMetaCell(imcell, icell)
            if res == imcell.instanced:
                instantiated.append(imcell)

        # instantiate the captured cells
        assert(len(do.op.captured) == len(cop.captured))
        for ccell, cap in zip(cop.captured, do.op.captured):
            if not ccell.instanced:
                self.debug("INSTc", ccell)
                _addInstantiated(ccell, cap)

        # instantiate the parameters (using the args)
        assert(len(do.args) == len(cop.params))
        for param, arg in zip(cop.params, do.args):
            self.debug("INSTp", param)
            _addInstantiated(param, arg)

        # instantiate the locals
        for loc in cop.locals:
            self.debug("LOC", debugString(loc))
            _addInstantiated(loc)

        # instantiate the does, set up continuations
        myNext = exNode.next
        cur = exNode
        for ms in cop.steps:
            self.debug("inst step: ", debugString(ms), " --- ", debugString(cop))
            step = M.ExecutionNode(do = inst.instantiateMetaDo(ms))
            step.parent = exNode
            cur.next = step
            cur = cur.next
        cur.next = myNext

        # uninstantiate the MetaCells we instantiated
        # important that this is *before* the steps execute, in order to support recursion (re-use of MetaCells)
        #  (this is not an in issue for a singleton, serialized, tail-recursive executor)
        #  (in multi-executor environment, we'd probably have to hold a lock at the cop object)
        for ms in instantiated:
            self.debug("unINST", debugString(ms))
            inst.uninstantiateMetaCell(ms)

        # continuation is set up and will be next executed
        self.debug("exec done, coming up:", exNode.next)
