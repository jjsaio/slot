
from . import model as M
from .fs import fs
from .logging import LoggingClass
from .util import prettyJson


class Compiler(LoggingClass):

    def __init__(self):
        LoggingClass.__init__(self)
        #self.setLevelDebug()

    def canCompile(obj):
        return obj and hasattr(obj, 'fsType') and hasattr(Compiler, "compile{}".format(fs.toString(obj.fsType)))

    def compile(self, obj, context):
        return getattr(self, "compile{}".format(fs.toString(obj.fsType)))(obj, context)

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

    def compileSlotDef(self, sd, context):
        assert(isinstance(sd, M.SlotDef))
        assert(not sd.compiled)
        slot = M.MetaSlot(slotType = self._slotType(sd.slotType, context))
        assert(slot.slotType)
        if sd.slop:
            assert(not sd.constant)
            slot.concrete = M.Slot(slotType = slot.slotType, data = self.compileSlopDef(sd.slop, context))
        elif sd.constant:
            slot.concrete = M.Slot(slotType = slot.slotType)
            slot.concrete.data = sd.constant[0] # can't use ctor since gencode uses `or None`
        if sd.name:
            slot.human = M.Human(name = sd.name)
            mslot = context.addNamedSlot(sd.name, slot)
        else:
            mslot = context.addSlot(slot)
        assert(isinstance(mslot, M.MetaSlot))
        sd.compiled = mslot
        return mslot

    def compileSlotRef(self, ref, context):
        assert(isinstance(ref, M.SlotRef))
        if ref.slot:
            assert(isinstance(ref.slot, M.SlotDef))
            slot = ref.slot.compiled
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

    def compileSlexDef(self, slex, context):
        assert(isinstance(slex, M.SlexDef))
        mslex = M.MetaSlex()
        mslex.op = self.compileSlotRef(slex.op, context)
        mslex.args = [ self.compileSlotRef(x, context) for x in slex.args ]
        return mslex

    def compileSlopDef(self, slopDef, context):
        assert(isinstance(slopDef, M.SlopDef))
        slop = M.Slop()
        slopContext = context.derive()

        for param in slopDef.params:
            assert(isinstance(param, M.SlotDef))
            slot = self.compileSlotDef(param, slopContext)
            assert(isinstance(slot, M.MetaSlot))
            slop.params.append(slot)

        for local in slopDef.locals:
            assert(isinstance(local, M.SlotDef))
            slot = self.compileSlotDef(local, slopContext)
            assert(isinstance(slot, M.MetaSlot))
            slop.locals.append(slot)

        self.debug("slop derived context:", slopContext.dump())

        for step in slopDef.steps:
            assert(isinstance(step, M.SlexDef))
            slex = self.compileSlexDef(step, slopContext)
            assert(isinstance(slex, M.MetaSlex))
            slop.steps.append(slex)

        return slop
