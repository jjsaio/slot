
from . import model as M
from .display import debugString
from .fs import fs
from .logging import LoggingClass
from .util import prettyJson


class Instantiator(LoggingClass):

    def __init__(self):
        LoggingClass.__init__(self)
        #self.setLevelDebug()

    def canInstantiate(obj):
        return obj and hasattr(obj, 'fsType') and hasattr(Instantiator, "instantiate{}".format(fs.toString(obj.fsType)))

    def instantiate(self, obj):
        return getattr(self, "instantiate{}".format(fs.toString(obj.fsType)))(obj)

    def instantiateMetaSlot(self, mslot, slot = None):
        assert(mslot and isinstance(mslot, M.MetaSlot))
        if mslot.instanced:
            raise Exception("MetaSlot `{}` is already instantiated in the current context".format(mslot.human.name if mslot.human else mslot))
        if mslot.concrete:
            if not isinstance(mslot.concrete.data, M.MetaSlop):
                return mslot.concrete
            # special handling for MetaSlops, need to be instantiated now
            slot = M.Slot(slotType = mslot.slotType,
                          data = self.instantiateMetaSlop(mslot.concrete.data),
                          human = mslot.human)
            assert(isinstance(slot.data, M.Slop))
        if slot:
            assert(isinstance(slot, M.Slot))
            mslot.instanced = slot
        else:
            mslot.instanced = M.Slot(slotType = mslot.slotType, human = mslot.human)
        self.debug("Instantiated: ", debugString(mslot), " ---> ", debugString(mslot.instanced), debugString(mslot.instanced.human))
        return mslot.instanced

    def uninstantiateMetaSlot(self, mslot):
        assert(mslot and isinstance(mslot, M.MetaSlot))
        self.debug("Uninstantiating: {}".format(mslot))
        assert(mslot.instanced)
        mslot.instanced = None

    def instantiatedSlot(self, mslot):
        assert(mslot and isinstance(mslot, M.MetaSlot))
        if mslot.instanced:
            return mslot.instanced
        elif mslot.concrete:
            return mslot.concrete
        else:
            raise Exception("Slot not instantiated: {}".format(debugString(mslot)))

    def instantiateMetaSlex(self, mslex):
        assert(isinstance(mslex, M.MetaSlex))
        opSlot = self.instantiatedSlot(mslex.op)
        assert(isinstance(opSlot, M.Slot))
        slop = opSlot.data
        if isinstance(slop, M.MetaSlop):
            assert(not slop.captured)
            slop = M.Slop(op = slop)
        slex = M.Slex(op = slop,
                      args = [ self.instantiatedSlot(a) for a in mslex.args ])
        self.debug("instantiated ", debugString(slex))
        return slex

    def instantiateMetaSlop(self, mslop):
        assert(isinstance(mslop, M.MetaSlop))
        return M.Slop(op = mslop,
                      captured = [ self.instantiatedSlot(c) for c in mslop.captured ])
