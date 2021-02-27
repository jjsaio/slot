
from . import model as M
from .logging import LoggingClass


class Context(LoggingClass):

    def __init__(self, parent = None):
        LoggingClass.__init__(self)
        self._parent = parent
        self._namedSlots = {}
        self._anonymousSlots = []

    def dump(self, all = False):
        lines = [ "Context @ {}".format(id(self)) ]
        for name in sorted(self._namedSlots.keys()):
            if (not all) and name.startswith('_'):
                continue
            s = self._namedSlots[name]
            if isinstance(s, M.Slot):
                lines.append("  {} -> {} => {}".format(name, displayStructure(s), displayStructure(s.data)))
            else:
                lines.append("  {} -> {}".format(name, displayStructure(s)))
        for slot in self._anonymousSlots:
            if isinstance(s, M.Slot):
                lines.append("  ANON  {} => {}".format(displayStructure(slot), displayStructure(slot.data)))
            else:
                lines.append("  ANON  {}".format(displayStructure(s)))
        return "\n".join(lines)

    def derive(self):
        return Context(self)

    def hasSlotNamed(self, n):
        return (n in self._namedSlots) or (self._parent and self._parent.hasSlotNamed(n))

    def slotNamed(self, n):
        return self._namedSlots.get(n, self._parent.slotNamed(n) if self._parent else None)

    def addNamedSlot(self, name, slot):
        if name in self._namedSlots:
            raise Exception("Slot already exists in context: `{}`".format(name))
        self._namedSlots[name] = slot
        return slot

    def addSlot(self, slot):
        self._anonymousSlots.append(slot)
        return slot
