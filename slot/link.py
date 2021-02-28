
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

    def link(self, obj, context):
        return getattr(self, "link{}".format(fs.toString(obj.fsType)))(obj, context)

    def _slotType(self, typeName, context):
        if not typeName:
            st = context.slotNamed('Generic').concrete
        elif not context.hasSlotNamed(typeName):
            raise Exception("Slot type not found in context: `{}`".format(typeName))
        else:
            st = context.slotNamed(typeName).concrete
        assert(isinstance(st, M.Slot))
        assert(isinstance(st.data, M.SlotType))
        return st.data

    def linkSlotDef(self, sd, context):
        assert(isinstance(sd, M.SlotDef))
        assert(not sd.linked)
        mslot = M.MetaSlot(slotType = self._slotType(sd.slotType, context))
        assert(mslot.slotType)
        if sd.name:
            mslot.human = M.Human(name = sd.name)
            context.addNamedSlot(sd.name, mslot)
        else:
            context.addSlot(mslot)
        if sd.slop:
            assert(not sd.constant)
            slop = self.linkSlopDef(sd.slop, context)
            slop.human = mslot.human
            mslot.concrete = M.Slot(slotType = mslot.slotType, data = slop, human = mslot.human)
        elif sd.constant:
            mslot.concrete = M.Slot(slotType = mslot.slotType)
            mslot.concrete.data = sd.constant[0] # can't use ctor since gencode uses `or None`
        assert(isinstance(mslot, M.MetaSlot))
        sd.linked = mslot
        return mslot

    def linkSlotRef(self, ref, context):
        assert(isinstance(ref, M.SlotRef))
        if ref.slot:
            assert(isinstance(ref.slot, M.SlotDef))
            slot = ref.slot.linked
        else:
            if not context.hasSlotNamed(ref.name):
                raise Exception("Unbound slot reference: `{}`".format(ref.name))
            slot = context.slotNamed(ref.name)
        assert(slot and isinstance(slot, M.MetaSlot))
        if slot.concrete:
            assert(isinstance(slot.concrete, M.Slot))
        if slot.instanced:
            # i think we should only ever be able to get here during interactive mode
            assert(isinstance(slot.instanced, M.Slot))
        return slot

    def linkSlexDef(self, slex, context):
        assert(isinstance(slex, M.SlexDef))
        mslex = M.MetaSlex()
        mslex.op = self.linkSlotRef(slex.op, context)
        mslex.args = [ self.linkSlotRef(x, context) for x in slex.args ]
        return mslex

    def linkSlopDef(self, slopDef, context):
        assert(isinstance(slopDef, M.SlopDef))
        slop = M.Slop()
        slopContext = context.derive()

        for param in slopDef.params:
            assert(isinstance(param, M.SlotDef))
            slot = self.linkSlotDef(param, slopContext)
            assert(isinstance(slot, M.MetaSlot))
            slop.params.append(slot)

        for local in slopDef.locals:
            assert(isinstance(local, M.SlotDef))
            slot = self.linkSlotDef(local, slopContext)
            assert(isinstance(slot, M.MetaSlot))
            slop.locals.append(slot)

        self.debug("slop derived context:", slopContext.dump())

        for step in slopDef.steps:
            assert(isinstance(step, M.SlexDef))
            slex = self.linkSlexDef(step, slopContext)
            assert(isinstance(slex, M.MetaSlex))
            slop.steps.append(slex)

        return slop
