
from . import model as M
from .logging import LoggingClass


class Instantiator(LoggingClass):

    def __init__(self):
        LoggingClass.__init__(self)
        #self.setLevelDebug()

    def _dropSlot(self, metaSlot):
        assert(metaSlot and isinstance(metaSlot, M.metaSlot))
        if s.instanced:
            # note this allows instanced to take precedence over concrete, e.g., a name was re-bound locally
            return s.instanced
        assert(s.concrete)
        return s.concrete

    # instantiate takes a MetaSlex to an array of Slex (e.g., each Slex corresponding to a step in the called Slop)
    def instantiate(self, mslex):
        assert(isinstance(mslex, M.MetaSlex))

        # get the slop
        slopSlot = self._dropSlot(mslex.op)
        slop = slopSlot.data
        if (not slop) or (not isinstance(slop, M.Slop)):
            raise Exception("Cannot instantiate Metaslex with non-Slop op: {}".format(slop))

        # set up the args/parameters:
        assert(len(mslex.args) == len(slop.params))
        for arg, param in zip(slex.args, slop.params):
            # set the metaslot to the passed-in arg
            assert(not param.instanced)
            # TODO: verify here that arg.slotType is compatible with orig.slotType 
            # the passed-in slot is to be used in this execution context
            param.instanced = self._dropSlot(arg)

        # create new slot instances for the locals
        for loc in slop.locals:
            assert(not loc.instanced)
            loc.instanced = M.Slot(slotType = loc.type, human = loc.human)

        # now instantiate all of the slexes
        self.debug("instantiate drop steps:", slop.steps)
        instantiated = []
        if slop.native:
            # for native ops, we instantiate the one slex that corresponds to calling the native op
            instantiated.append(M.Slex(op = slopSlot,
                                       args = [ p.instanced for p in slop.params ],
                                       human = mslex.human))
        else:
            for step in slop.steps:
                assert(isinstance(step, M.MetaSlex))
                instantiated.append(M.Slex(op = self._dropSlot(step.op),
                                           args = [ self._dropSlot(a) for a in step.args ],
                                           human = step.human))

        # clear the instanced slots, since they're all set up in the
        # instantiated ones now
        for ms in slop.params + slop.locals:
            ms.instanced = None

        return instantiated
