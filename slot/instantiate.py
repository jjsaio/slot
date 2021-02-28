
from . import model as M
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
        if mslot.concrete:
            assert(not mslot.instanced)
            return mslot.concrete
        if mslot.instanced:
            raise Exception("MetaSlot `{}` is already instantiated in the current context".format(mslot.human.name if mslot.human else mslot))
        if slot:
            assert(isinstance(slot, M.Slot))
            mslot.instanced = slot
        else:
            mslot.instanced = M.Slot(slotType = mslot.slotType, human = mslot.human)
        return mslot.instanced

    def uninstantiateMetaSlot(self, mslot):
        assert(mslot and isinstance(mslot, M.MetaSlot))
        assert(mslot.instanced)
        mslot.instanced = None

    def instantiatedSlot(self, mslot):
        assert(mslot and isinstance(mslot, M.MetaSlot))
        assert(not (mslot.concrete and mslot.instanced)) # pretty sure concrete/instanced needs to be strictly either-or
        if mslot.concrete:
            return mslot.concrete
        elif mslot.instanced:
            return mslot.instanced
        else:
            raise Exception("Slot not instantiated: {}".format(mslot.human.name if mslot.human else mslot.json()))

    def instantiateMetaSlex(self, mslex):
        assert(isinstance(mslex, M.MetaSlex))
        opSlot = self.instantiatedSlot(mslex.op)
        assert(isinstance(opSlot, M.Slot) and isinstance(opSlot.data, M.Slop))
        return M.Slex(op = opSlot.data,
                      args = [ self.instantiatedSlot(a) for a in mslex.args ])
