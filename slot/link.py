
from . import model as M
from .display import debugString
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
        concrete = None
        if sd.slop:
            assert(not sd.constant)
            concrete = self.linkSlopDef(sd.slop, namespace)
            concrete.human = mslot.human
        elif sd.constant:
            concrete = sd.constant[0]
        if concrete:
            mslot.concrete = M.Slot(slotType = mslot.slotType, human = mslot.human)
            mslot.concrete.data = concrete # can't use ctor since gencode uses `or None`
        assert(isinstance(mslot, M.MetaSlot))
        sd.linked = mslot
        return mslot

    def linkSlotRef(self, ref, namespace):
        assert(isinstance(ref, M.SlotRef))
        if ref.slot:
            assert(isinstance(ref.slot, M.SlotDef))
            slot = ref.slot.linked
            if ref.name and (not slot.human):
                # primarily for allowing anonymous slots to be named, for debugging purposes
                slot.human = M.Human(name = ref.name)
        else:
            if not namespace.hasSlotNamed(ref.name):
                raise Exception("Unbound slot reference: `{}`".format(ref.name))
            slot = namespace.slotNamed(ref.name)
        assert(slot and isinstance(slot, M.MetaSlot))
        if slot.concrete:
            assert(isinstance(slot.concrete, M.Slot))
        elif not namespace.ownsSlot(slot, name = ref.name):
            namespace.capture(slot)
        if slot.instanced:
            # i think we should only ever be able to get here during interactive mode
            assert(isinstance(slot.instanced, M.Slot))
        self.debug("linked SR:", debugString(slot))
        return slot

    def linkSlexDef(self, slex, namespace):
        assert(isinstance(slex, M.SlexDef))
        mslex = M.MetaSlex()
        mslex.op = self.linkSlotRef(slex.op, namespace)
        mslex.args = [ self.linkSlotRef(x, namespace) for x in slex.args ]
        return mslex

    def linkSlopDef(self, slopDef, namespace):
        assert(isinstance(slopDef, M.SlopDef))
        slop = M.MetaSlop()
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

        for slot in slopNamespace.capturedSlots:
            self.debug("{} captured {}".format(debugString(slop), debugString(slot)))
            assert(isinstance(slot, M.MetaSlot))
            slop.captured.append(slot)

        return slop
