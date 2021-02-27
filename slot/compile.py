
from . import model as M
from .fs import fs
from .logging import LoggingClass


class Compiler(LoggingClass):

    def __init__(self):
        LoggingClass.__init__(self)
        #self.setLevelDebug()

    def canCompile(obj):
        return obj and hasattr(obj, 'fsType') and hasattr(self, "compile{}".format(fs.toString(obj.fsType)))

    def compile(self, obj, context):
        return getattr(self, "compile{}".format(fs.toString(obj.fsType)))(obj, context)

    def _slotType(self, typeName, context):
        if not arg:
            return context.slotNamed('Generic')
        if not context.hasSlotNamed(typeName):
            raise Exception("Slot type not found in context: `{}`".format(typeName))
        return context.slotNamed(typeName)

    def compileSlotDef(self, sd, context):
        assert(isinstance(sd, M.SlotDef))
        slot = M.MetaSlot(slotType = self._slotType(sd.slotType, context))
        if sd.constant:
            slot.concrete = M.Slot(slotType = slot.slotType, data = sd.constant)
            return context.addSlot(slot)
        else:
            slot.human = M.Human(name = sd.name)
            return context.addNamedSlot(sd.name, slot)

    def compileSlotRef(self, ref, context):
        assert(isinstance(ref, M.SlotRef))
        if ref.slex:
            assert(isinstance(ref.slex, M.SlexDef))
            slex = self.compileSlotDef(ref.slex)
            assert(isinstance(slex, M.MetaSlex))
            slot = M.MetaSlot(slotType = context.slotNamed('MetaSlex'), concrete = slex)
        elif ref.slop:
            assert(isinstance(ref.slex, M.SlopDef))
            slop = self.compileSlopDef(ref.slop)
            assert(isinstance(slop, M.Slop))
            slot = M.MetaSlot(slotType = context.slotNamed('Slop'), concrete = slop)
        elif ref.slot:
            assert(isinstance(ref.slot, M.SlotDef))
            slot = self.compileSlotDef(ref.slot)
        else:
            if not context.hasSlotNamed(ref.name):
                raise Exception("Unbound slot reference: `{}`".format(ref.name))
            slot = context.slotNamed(ref.name)
        assert(isinstance(slot, M.MetaSlot))
        return slot

    def compileSlexDef(self, slex, context):
        assert(isinstance(slex, M.SlexDef))
        slex = M.MetaSlex()
        slex.op = self.compileSlotRef(slex.op, context)
        slex.args = [ self.compileSlotRef(x, context) for x in slex.args ]
        return slex

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
