
from . import model as M
from .display import debugString
from .fs import fs
from .logging import LoggingClass
from .util import prettyJson


class Instantiator(LoggingClass):

    def __init__(self):
        LoggingClass.__init__(self)
        #self.setLevelDebug()

    def canInstantiate(obj):
        return obj and hasattr(obj, 'fsType') and hasattr(Instantiator, "instantiate{}".format(fs.toString(obj.fsType)))

    def instantiate(self, obj):
        return getattr(self, "instantiate{}".format(fs.toString(obj.fsType)))(obj)

    def instantiateMetaCell(self, mcell, cell = None):
        assert(mcell and isinstance(mcell, M.MetaCell))
        if mcell.instanced:
            raise Exception("MetaCell `{}` is already instantiated in the current context".format(mcell.human.name if mcell.human else mcell))
        if mcell.concrete:
            if not isinstance(mcell.concrete.data, M.MetaCop):
                return mcell.concrete
            # special handling for MetaCops, need to be instantiated now
            cell = M.Cell(cellType = mcell.cellType,
                          data = self.instantiateMetaCop(mcell.concrete.data),
                          human = mcell.human)
            assert(isinstance(cell.data, M.Cop))
        if cell:
            assert(isinstance(cell, M.Cell))
            mcell.instanced = cell
        else:
            mcell.instanced = M.Cell(cellType = mcell.cellType, human = mcell.human)
        self.debug("Instantiated: ", debugString(mcell), " ---> ", debugString(mcell.instanced), debugString(mcell.instanced.human))
        return mcell.instanced

    def uninstantiateMetaCell(self, mcell):
        assert(mcell and isinstance(mcell, M.MetaCell))
        self.debug("Uninstantiating: {}".format(mcell))
        assert(mcell.instanced)
        mcell.instanced = None

    def instantiatedCell(self, mcell):
        assert(mcell and isinstance(mcell, M.MetaCell))
        if mcell.instanced:
            return mcell.instanced
        elif mcell.concrete:
            return mcell.concrete
        else:
            raise Exception("Cell not instantiated: {}".format(debugString(mcell)))

    def instantiateMetaDo(self, mdo):
        assert(isinstance(mdo, M.MetaDo))
        opCell = self.instantiatedCell(mdo.op)
        assert(isinstance(opCell, M.Cell))
        cop = opCell.data
        if isinstance(cop, M.MetaCop):
            cop = M.Cop(op = cop,
                        captured = [ self.instantiatedCell(c) for c in cop.captured ])
        do = M.Do(op = cop,
                  args = [ self.instantiatedCell(a) for a in mdo.args ])
        self.debug("instantiated ", debugString(do))
        return do

    def instantiateMetaCop(self, mcop):
        assert(isinstance(mcop, M.MetaCop))
        return M.Cop(op = mcop,
                      captured = [ self.instantiatedCell(c) for c in mcop.captured ])
