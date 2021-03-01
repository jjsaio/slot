
from .logging import LoggingClass, initializeLogging

initializeLogging(format = LoggingClass.noStampFormat)

def interactive():
    from .interactive import Interactive
    Interactive().go()

def run(path):
    from .interpret import Interpreter
    Interpreter().run(path)

i = interactive
