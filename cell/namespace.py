
from . import model as M
from .display import displayStructure, displayDesignation
from .logging import LoggingClass


class Namespace(LoggingClass):

    def __init__(self, parent = None):
        LoggingClass.__init__(self)
        self._parent = parent
        self._namedCells = {}
        self._anonymousCells = []
        self._captured = []

    def dump(self, all = False):
        lines = [ "Namespace @ {}".format(id(self)) ]
        cells = [ (name, self._namedCells[name]) for name in sorted(self._namedCells.keys()) ] + [ (None, s) for s in self._anonymousCells ]
        for name, mcell in cells:
            assert(isinstance(mcell, M.MetaCell))
            line = ' "{}"'.format(name) if name else "  ANON"
            line += ("\t" + displayStructure(mcell))
            cell = mcell.concrete or mcell.instanced
            if cell:
                line += "\t:  {} \t=> \t{}".format(displayStructure(cell), displayDesignation(cell))
            lines.append(line)
        dmp = "\n".join(lines)
        if all and self._parent:
            dmp += ("\nParent " + self._parent.dump(all = True))
        return dmp

    def derive(self):
        return Namespace(self)

    def hasCellNamed(self, n):
        return (n in self._namedCells) or (self._parent and self._parent.hasCellNamed(n))

    def cellNamed(self, n):
        return self._namedCells.get(n, self._parent.cellNamed(n) if self._parent else None)

    def addNamedCell(self, name, cell):
        assert(not name.startswith('['))
        if name in self._namedCells:
            raise Exception("Cell already exists in namespace: `{}`".format(name))
        assert(isinstance(cell, M.MetaCell))
        self._namedCells[name] = cell
        return cell

    def addCell(self, cell):
        assert(isinstance(cell, M.MetaCell))
        self._anonymousCells.append(cell)
        return cell

    def ownsCell(self, cell, name = None):
        if name and (self._namedCells.get(name) == cell):
            return True
        # could improve this if necc with an id-based lookup
        return (cell in self._namedCells.values()) or (cell in self._anonymousCells)

    def capture(self, cell):
        assert(isinstance(cell, M.MetaCell))
        assert(not self.ownsCell(cell))
        if cell in self._captured:
            return
        self._captured.append(cell)
        if self._parent and (not self._parent.ownsCell(cell)):
            self._parent.capture(cell)

    @property
    def capturedCells(self):
        return self._captured
