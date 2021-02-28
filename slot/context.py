
from . import model as M
from .display import displayStructure, displayDesignation
from .logging import LoggingClass


class Context(LoggingClass):

    def __init__(self, parent = None):
        LoggingClass.__init__(self)
        self._parent = parent
        self._namedSlots = {}
        self._anonymousSlots = []

    def dump(self, all = False):
        lines = [ "Context @ {}".format(id(self)) ]
        slots = [ (name, self._namedSlots[name]) for name in sorted(self._namedSlots.keys()) ] + [ (None, s) for s in self._anonymousSlots ]
        for name, mslot in slots:
            assert(isinstance(mslot, M.MetaSlot))
            line = ' "{}"'.format(name) if name else "  ANON"
            line += ("\t" + displayStructure(mslot))
            slot = mslot.concrete or mslot.instanced
            if slot:
                line += "\t:  {} \t=> \t{}".format(displayStructure(slot), displayDesignation(slot))
            lines.append(line)
        dmp = "\n".join(lines)
        if all and self._parent:
            dmp += ("\nParent " + self._parent.dump(all = True))
        return dmp

    def derive(self):
        return Context(self)

    def hasSlotNamed(self, n):
        return (n in self._namedSlots) or (self._parent and self._parent.hasSlotNamed(n))

    def slotNamed(self, n):
        return self._namedSlots.get(n, self._parent.slotNamed(n) if self._parent else None)

    def addNamedSlot(self, name, slot):
        assert(not name.startswith('['))
        if name in self._namedSlots:
            raise Exception("Slot already exists in context: `{}`".format(name))
        assert(isinstance(slot, M.MetaSlot))
        self._namedSlots[name] = slot
        return slot

    def addSlot(self, slot):
        assert(isinstance(slot, M.MetaSlot))
        self._anonymousSlots.append(slot)
        return slot
