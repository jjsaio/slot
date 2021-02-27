
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
        return st

    def compileSlotDef(self, sd, context):
        assert(isinstance(sd, M.SlotDef))
        slot = M.MetaSlot(slotType = self._slotType(sd.slotType, context))
        if sd.constant is not None:
            slot.concrete = M.Slot(slotType = slot.slotType)
            slot.concrete.data = sd.constant # can't use ctor since gencode uses `or None`
            return context.addSlot(slot)
        else:
            slot.human = M.Human(name = sd.name)
            return context.addNamedSlot(sd.name, slot)

    def compileSlotRef(self, ref, context):
        assert(isinstance(ref, M.SlotRef))
        if ref.slop:
            assert(isinstance(ref.slop, M.SlopDef))
            slop = self.compileSlopDef(ref.slop, context)
            assert(isinstance(slop, M.Slop))
            c = M.Slot(slotType = context.slotNamed('Slop'), data = slop)
            slot = M.MetaSlot(slotType = c.slotType, concrete = c)
        elif ref.slot:
            assert(isinstance(ref.slot, M.SlotDef))
            slot = self.compileSlotDef(ref.slot, context)
        else:
            if not context.hasSlotNamed(ref.name):
                raise Exception("Unbound slot reference: `{}`".format(ref.name))
            slot = context.slotNamed(ref.name)
        assert(isinstance(slot, M.MetaSlot))
        if slot.concrete:
            assert(isinstance(slot.concrete, M.Slot))
        if slot.instanced:
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
