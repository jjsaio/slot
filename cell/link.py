
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

    def _cellType(self, typeName, namespace):
        if not typeName:
            st = namespace.cellNamed('Generic').concrete
        elif not namespace.hasCellNamed(typeName):
            raise Exception("Cell type not found in namespace: `{}`".format(typeName))
        else:
            st = namespace.cellNamed(typeName).concrete
        assert(isinstance(st, M.Cell))
        assert(isinstance(st.data, M.CellType))
        return st.data

    def linkCellDef(self, sd, namespace):
        assert(isinstance(sd, M.CellDef))
        assert(not sd.linked)
        mcell = M.MetaCell(cellType = self._cellType(sd.cellType, namespace))
        assert(mcell.cellType)
        if sd.name:
            mcell.human = M.Human(name = sd.name)
            namespace.addNamedCell(sd.name, mcell)
        else:
            namespace.addCell(mcell)
        concrete = None
        if sd.cop:
            assert(not sd.constant)
            concrete = self.linkCopDef(sd.cop, namespace)
            concrete.human = mcell.human
        elif sd.constant:
            concrete = sd.constant[0]
        if concrete:
            mcell.concrete = M.Cell(cellType = mcell.cellType, human = mcell.human)
            mcell.concrete.data = concrete # can't use ctor since gencode uses `or None`
        assert(isinstance(mcell, M.MetaCell))
        sd.linked = mcell
        return mcell

    def linkCellRef(self, ref, namespace):
        assert(isinstance(ref, M.CellRef))
        if ref.cell:
            assert(isinstance(ref.cell, M.CellDef))
            cell = ref.cell.linked
            if ref.name and (not cell.human):
                # primarily for allowing anonymous cells to be named, for debugging purposes
                cell.human = M.Human(name = ref.name)
        else:
            if not namespace.hasCellNamed(ref.name):
                raise Exception("Unbound cell reference: `{}`".format(ref.name))
            cell = namespace.cellNamed(ref.name)
        assert(cell and isinstance(cell, M.MetaCell))
        if cell.concrete:
            assert(isinstance(cell.concrete, M.Cell))
        elif not namespace.ownsCell(cell, name = ref.name):
            namespace.capture(cell)
        if cell.instanced:
            # i think we should only ever be able to get here during interactive mode
            assert(isinstance(cell.instanced, M.Cell))
        self.debug("linked SR:", debugString(cell))
        return cell

    def linkDoDef(self, do, namespace):
        assert(isinstance(do, M.DoDef))
        mdo = M.MetaDo()
        mdo.op = self.linkCellRef(do.op, namespace)
        mdo.args = [ self.linkCellRef(x, namespace) for x in do.args ]
        return mdo

    def linkCopDef(self, copDef, namespace):
        assert(isinstance(copDef, M.CopDef))
        cop = M.MetaCop()
        copNamespace = namespace.derive()

        for param in copDef.params:
            assert(isinstance(param, M.CellDef))
            cell = self.linkCellDef(param, copNamespace)
            assert(isinstance(cell, M.MetaCell))
            cop.params.append(cell)

        for local in copDef.locals:
            assert(isinstance(local, M.CellDef))
            cell = self.linkCellDef(local, copNamespace)
            assert(isinstance(cell, M.MetaCell))
            cop.locals.append(cell)

        self.debug("cop derived namespace:", copNamespace.dump())

        for step in copDef.steps:
            assert(isinstance(step, M.DoDef))
            do = self.linkDoDef(step, copNamespace)
            assert(isinstance(do, M.MetaDo))
            cop.steps.append(do)

        for cell in copNamespace.capturedCells:
            self.debug("{} captured {}".format(debugString(cop), debugString(cell)))
            assert(isinstance(cell, M.MetaCell))
            cop.captured.append(cell)

        return cop
