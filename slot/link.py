
from . import model as M
from .fs import fs
from .logging import LoggingClass
from .util import prettyJson


class Linker(LoggingClass):

    def __init__(self):
        LoggingClass.__init__(self)
        #self.setLevelDebug()

    def canLink(obj):
        return obj and hasattr(obj, 'fsType') and hasattr(Linker, "link{}".format(fs.toString(obj.fsType)))

    def link(self, obj, namespace):
        return getattr(self, "link{}".format(fs.toString(obj.fsType)))(obj, namespace)

    def _slotType(self, typeName, namespace):
        if not typeName:
            st = namespace.slotNamed('Generic').concrete
        elif not namespace.hasSlotNamed(typeName):
            raise Exception("Slot type not found in namespace: `{}`".format(typeName))
        else:
            st = namespace.slotNamed(typeName).concrete
        assert(isinstance(st, M.Slot))
        assert(isinstance(st.data, M.SlotType))
        return st.data

    def linkSlotDef(self, sd, namespace):
        assert(isinstance(sd, M.SlotDef))
        assert(not sd.linked)
        mslot = M.MetaSlot(slotType = self._slotType(sd.slotType, namespace))
        assert(mslot.slotType)
        if sd.name:
            mslot.human = M.Human(name = sd.name)
            namespace.addNamedSlot(sd.name, mslot)
        else:
            namespace.addSlot(mslot)
        if sd.slop:
            assert(not sd.constant)
            slop = self.linkSlopDef(sd.slop, namespace)
            slop.human = mslot.human
            mslot.concrete = M.Slot(slotType = mslot.slotType, data = slop, human = mslot.human)
        elif sd.constant:
            mslot.concrete = M.Slot(slotType = mslot.slotType)
            mslot.concrete.data = sd.constant[0] # can't use ctor since gencode uses `or None`
        assert(isinstance(mslot, M.MetaSlot))
        sd.linked = mslot
        return mslot

    def linkSlotRef(self, ref, namespace):
        assert(isinstance(ref, M.SlotRef))
        if ref.slot:
            assert(isinstance(ref.slot, M.SlotDef))
            slot = ref.slot.linked
        else:
            if not namespace.hasSlotNamed(ref.name):
                raise Exception("Unbound slot reference: `{}`".format(ref.name))
            slot = namespace.slotNamed(ref.name)
        assert(slot and isinstance(slot, M.MetaSlot))
        if slot.concrete:
            assert(isinstance(slot.concrete, M.Slot))
        if slot.instanced:
            # i think we should only ever be able to get here during interactive mode
            assert(isinstance(slot.instanced, M.Slot))
        return slot

    def linkSlexDef(self, slex, namespace):
        assert(isinstance(slex, M.SlexDef))
        mslex = M.MetaSlex()
        mslex.op = self.linkSlotRef(slex.op, namespace)
        mslex.args = [ self.linkSlotRef(x, namespace) for x in slex.args ]
        return mslex

    def linkSlopDef(self, slopDef, namespace):
        assert(isinstance(slopDef, M.SlopDef))
        slop = M.Slop()
        slopNamespace = namespace.derive()

        for param in slopDef.params:
            assert(isinstance(param, M.SlotDef))
            slot = self.linkSlotDef(param, slopNamespace)
            assert(isinstance(slot, M.MetaSlot))
            slop.params.append(slot)

        for local in slopDef.locals:
            assert(isinstance(local, M.SlotDef))
            slot = self.linkSlotDef(local, slopNamespace)
            assert(isinstance(slot, M.MetaSlot))
            slop.locals.append(slot)

        self.debug("slop derived namespace:", slopNamespace.dump())

        for step in slopDef.steps:
            assert(isinstance(step, M.SlexDef))
            slex = self.linkSlexDef(step, slopNamespace)
            assert(isinstance(slex, M.MetaSlex))
            slop.steps.append(slex)

        return slop
