
from . import model as M


def _displayType(x):
    return (x.human.displayType or "??") if (x and x.human) else "??"

def displayStructure(x):
    t = type(x).__name__
    if isinstance(x, M.Slot) or isinstance(x, M.MetaSlot):
        d = _displayType(x.slotType)
    elif isinstance(x, M.Slop):
        d = "..." # TBD
    elif isinstance(x, M.Slex):
        d = "..."  # TBD
    elif callable(x):
        d = impl.__name__
    elif hasattr(x, 'json'):
        d = x.json()
        d = str(d)
        if len(d) > 32:
            d = d[:28] + "...}"
    else:
        d = repr(x)
    return "<{}:{}>".format(t, d)
