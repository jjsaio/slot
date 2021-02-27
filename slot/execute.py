
from . import model as M
from .logging import LoggingClass


class Executor(LoggingClass):

    def __init__(self):
        LoggingClass.__init__(self)
        #self.setLevelDebug()

    def canExecute(obj):
        return obj and isinstance(obj, M.Slex)

    def execute(self, slex):
        assert(isinstance(slex, M.Slex))
        


