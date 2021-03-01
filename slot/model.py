import sys

from .fs import fs


class ExecutionContext(object):

    def __init__(self, interpreter = None, node = None):
        self.interpreter = interpreter or None  # type Interpreter
        self.node = node or None  # type ExecutionNode

    @property
    def typeName(self):
        return "ExecutionContext"

    @property
    def fsType(self):
        return fs.ExecutionContext

    def defaultDict(self):
        return {
            'interpreter' : self.interpreter or None,
            'node' : self.node or None,
        }

    def _description(self):
        return "ExecutionContext: `{}`".format(", ".join([ "{}={}".format(k, v) for k, v in self.json(skipTypes = True).items() ]))

    def _newObjectOfSameType(self):
        return ExecutionContext()

    def clone(self):
        c = self._newObjectOfSameType()
        if hasattr(self, 'serialize'):
            c.deserialize(self.serialize())
        else:
            c.loadFromJson(self.json())
        return c

    def loadFromJson(self, json):
        if not json:
            return self
        self.interpreter = Interpreter().loadFromJson(json.get('interpreter'))
        self.node = ExecutionNode().loadFromJson(json.get('node'))
        return self

    def json(self, skipTypes = False):
        d = { }
        if not skipTypes:
            d["type"] = self.typeName
        if self.interpreter != None: d['interpreter'] = self.interpreter.json(skipTypes = skipTypes) if hasattr(self.interpreter, 'json') else id(self.interpreter)
        if self.node != None: d['node'] = self.node.json(skipTypes = skipTypes) if hasattr(self.node, 'json') else id(self.node)
        return d

class ExecutionNode(object):

    def __init__(self, slex = None, executed = None, next = None, parent = None):
        self.slex = slex or None  # type Slex
        self.executed = executed or False  # type Boolean
        self.next = next or None  # type ExecutionNode
        self.parent = parent or None  # type ExecutionNode

    @property
    def typeName(self):
        return "ExecutionNode"

    @property
    def fsType(self):
        return fs.ExecutionNode

    def defaultDict(self):
        return {
            'slex' : self.slex or None,
            'executed' : self.executed or False,
            'next' : self.next or None,
            'parent' : self.parent or None,
        }

    def _description(self):
        return "ExecutionNode: `{}`".format(", ".join([ "{}={}".format(k, v) for k, v in self.json(skipTypes = True).items() ]))

    def _newObjectOfSameType(self):
        return ExecutionNode()

    def clone(self):
        c = self._newObjectOfSameType()
        if hasattr(self, 'serialize'):
            c.deserialize(self.serialize())
        else:
            c.loadFromJson(self.json())
        return c

    def loadFromJson(self, json):
        if not json:
            return self
        self.slex = Slex().loadFromJson(json.get('slex'))
        self.executed = json.get('executed')
        self.next = ExecutionNode().loadFromJson(json.get('next'))
        self.parent = ExecutionNode().loadFromJson(json.get('parent'))
        return self

    def json(self, skipTypes = False):
        d = { }
        if not skipTypes:
            d["type"] = self.typeName
        if self.slex != None: d['slex'] = self.slex.json(skipTypes = skipTypes) if hasattr(self.slex, 'json') else id(self.slex)
        if self.executed != None: d['executed'] = self.executed
        if self.next != None: d['next'] = self.next.json(skipTypes = skipTypes) if hasattr(self.next, 'json') else id(self.next)
        if self.parent != None: d['parent'] = self.parent.json(skipTypes = skipTypes) if hasattr(self.parent, 'json') else id(self.parent)
        return d

class SlotType(object):

    def __init__(self, nativeType = None, human = None):
        self.nativeType = nativeType or None  # type Object
        self.human = human or None  # type Human

    @property
    def typeName(self):
        return "SlotType"

    @property
    def fsType(self):
        return fs.SlotType

    def defaultDict(self):
        return {
            'nativeType' : self.nativeType or None,
            'human' : self.human or None,
        }

    def _description(self):
        return "SlotType: `{}`".format(", ".join([ "{}={}".format(k, v) for k, v in self.json(skipTypes = True).items() ]))

    def _newObjectOfSameType(self):
        return SlotType()

    def clone(self):
        c = self._newObjectOfSameType()
        if hasattr(self, 'serialize'):
            c.deserialize(self.serialize())
        else:
            c.loadFromJson(self.json())
        return c

    def loadFromJson(self, json):
        if not json:
            return self
        self.nativeType = Object().loadFromJson(json.get('nativeType'))
        self.human = Human().loadFromJson(json.get('human'))
        return self

    def json(self, skipTypes = False):
        d = { }
        if not skipTypes:
            d["type"] = self.typeName
        if self.nativeType != None: d['nativeType'] = self.nativeType.json(skipTypes = skipTypes) if hasattr(self.nativeType, 'json') else id(self.nativeType)
        if self.human != None: d['human'] = self.human.json(skipTypes = skipTypes) if hasattr(self.human, 'json') else id(self.human)
        return d

class Slot(object):

    def __init__(self, slotType = None, data = None, human = None):
        self.slotType = slotType or None  # type SlotType
        self.data = data or None  # type Pointer
        self.human = human or None  # type Human

    @property
    def typeName(self):
        return "Slot"

    @property
    def fsType(self):
        return fs.Slot

    def defaultDict(self):
        return {
            'slotType' : self.slotType or None,
            'data' : self.data or None,
            'human' : self.human or None,
        }

    def _description(self):
        return "Slot: `{}`".format(", ".join([ "{}={}".format(k, v) for k, v in self.json(skipTypes = True).items() ]))

    def _newObjectOfSameType(self):
        return Slot()

    def clone(self):
        c = self._newObjectOfSameType()
        if hasattr(self, 'serialize'):
            c.deserialize(self.serialize())
        else:
            c.loadFromJson(self.json())
        return c

    def loadFromJson(self, json):
        if not json:
            return self
        self.slotType = SlotType().loadFromJson(json.get('slotType'))
        self.data = json.get('data')
        self.human = Human().loadFromJson(json.get('human'))
        return self

    def json(self, skipTypes = False):
        d = { }
        if not skipTypes:
            d["type"] = self.typeName
        if self.slotType != None: d['slotType'] = self.slotType.json(skipTypes = skipTypes) if hasattr(self.slotType, 'json') else id(self.slotType)
        if self.data != None: d['data'] = id(self.data)
        if self.human != None: d['human'] = self.human.json(skipTypes = skipTypes) if hasattr(self.human, 'json') else id(self.human)
        return d

class Slex(object):

    def __init__(self, op = None, args = None):
        self.op = op or None  # type Slop
        self.args = args or []  # type [Slot]

    @property
    def typeName(self):
        return "Slex"

    @property
    def fsType(self):
        return fs.Slex

    def defaultDict(self):
        return {
            'op' : self.op or None,
            'args' : self.args or [],
        }

    def _description(self):
        return "Slex: `{}`".format(", ".join([ "{}={}".format(k, v) for k, v in self.json(skipTypes = True).items() ]))

    def _newObjectOfSameType(self):
        return Slex()

    def clone(self):
        c = self._newObjectOfSameType()
        if hasattr(self, 'serialize'):
            c.deserialize(self.serialize())
        else:
            c.loadFromJson(self.json())
        return c

    def loadFromJson(self, json):
        if not json:
            return self
        self.op = Slop().loadFromJson(json.get('op'))
        self.args = [ Slot().loadFromJson(x) for x in json.get('args') or [] ]
        return self

    def json(self, skipTypes = False):
        d = { }
        if not skipTypes:
            d["type"] = self.typeName
        if self.op != None: d['op'] = self.op.json(skipTypes = skipTypes) if hasattr(self.op, 'json') else id(self.op)
        if self.args != None: d['args'] = [ x.json(skipTypes = skipTypes) for x in self.args ]
        return d

class Slop(object):

    def __init__(self, op = None, captured = None):
        self.op = op or None  # type MetaSlop
        self.captured = captured or []  # type [Slot]

    @property
    def typeName(self):
        return "Slop"

    @property
    def fsType(self):
        return fs.Slop

    def defaultDict(self):
        return {
            'op' : self.op or None,
            'captured' : self.captured or [],
        }

    def _description(self):
        return "Slop: `{}`".format(", ".join([ "{}={}".format(k, v) for k, v in self.json(skipTypes = True).items() ]))

    def _newObjectOfSameType(self):
        return Slop()

    def clone(self):
        c = self._newObjectOfSameType()
        if hasattr(self, 'serialize'):
            c.deserialize(self.serialize())
        else:
            c.loadFromJson(self.json())
        return c

    def loadFromJson(self, json):
        if not json:
            return self
        self.op = MetaSlop().loadFromJson(json.get('op'))
        self.captured = [ Slot().loadFromJson(x) for x in json.get('captured') or [] ]
        return self

    def json(self, skipTypes = False):
        d = { }
        if not skipTypes:
            d["type"] = self.typeName
        if self.op != None: d['op'] = self.op.json(skipTypes = skipTypes) if hasattr(self.op, 'json') else id(self.op)
        if self.captured != None: d['captured'] = [ x.json(skipTypes = skipTypes) for x in self.captured ]
        return d

class MetaSlop(object):

    def __init__(self, params = None, captured = None, locals = None, steps = None, native = None, human = None):
        self.params = params or []  # type [MetaSlot]
        self.captured = captured or []  # type [MetaSlot]
        self.locals = locals or []  # type [MetaSlot]
        self.steps = steps or []  # type [MetaSlex]
        self.native = native or None  # type Object
        self.human = human or None  # type Human

    @property
    def typeName(self):
        return "MetaSlop"

    @property
    def fsType(self):
        return fs.MetaSlop

    def defaultDict(self):
        return {
            'params' : self.params or [],
            'captured' : self.captured or [],
            'locals' : self.locals or [],
            'steps' : self.steps or [],
            'native' : self.native or None,
            'human' : self.human or None,
        }

    def _description(self):
        return "MetaSlop: `{}`".format(", ".join([ "{}={}".format(k, v) for k, v in self.json(skipTypes = True).items() ]))

    def _newObjectOfSameType(self):
        return MetaSlop()

    def clone(self):
        c = self._newObjectOfSameType()
        if hasattr(self, 'serialize'):
            c.deserialize(self.serialize())
        else:
            c.loadFromJson(self.json())
        return c

    def loadFromJson(self, json):
        if not json:
            return self
        self.params = [ MetaSlot().loadFromJson(x) for x in json.get('params') or [] ]
        self.captured = [ MetaSlot().loadFromJson(x) for x in json.get('captured') or [] ]
        self.locals = [ MetaSlot().loadFromJson(x) for x in json.get('locals') or [] ]
        self.steps = [ MetaSlex().loadFromJson(x) for x in json.get('steps') or [] ]
        self.native = Object().loadFromJson(json.get('native'))
        self.human = Human().loadFromJson(json.get('human'))
        return self

    def json(self, skipTypes = False):
        d = { }
        if not skipTypes:
            d["type"] = self.typeName
        if self.params != None: d['params'] = [ x.json(skipTypes = skipTypes) for x in self.params ]
        if self.captured != None: d['captured'] = [ x.json(skipTypes = skipTypes) for x in self.captured ]
        if self.locals != None: d['locals'] = [ x.json(skipTypes = skipTypes) for x in self.locals ]
        if self.steps != None: d['steps'] = [ x.json(skipTypes = skipTypes) for x in self.steps ]
        if self.native != None: d['native'] = self.native.json(skipTypes = skipTypes) if hasattr(self.native, 'json') else id(self.native)
        if self.human != None: d['human'] = self.human.json(skipTypes = skipTypes) if hasattr(self.human, 'json') else id(self.human)
        return d

class MetaSlot(object):

    def __init__(self, slotType = None, concrete = None, instanced = None, human = None):
        self.slotType = slotType or None  # type Slot
        self.concrete = concrete or None  # type Slot
        self.instanced = instanced or None  # type Slot
        self.human = human or None  # type Human

    @property
    def typeName(self):
        return "MetaSlot"

    @property
    def fsType(self):
        return fs.MetaSlot

    def defaultDict(self):
        return {
            'slotType' : self.slotType or None,
            'concrete' : self.concrete or None,
            'instanced' : self.instanced or None,
            'human' : self.human or None,
        }

    def _description(self):
        return "MetaSlot: `{}`".format(", ".join([ "{}={}".format(k, v) for k, v in self.json(skipTypes = True).items() ]))

    def _newObjectOfSameType(self):
        return MetaSlot()

    def clone(self):
        c = self._newObjectOfSameType()
        if hasattr(self, 'serialize'):
            c.deserialize(self.serialize())
        else:
            c.loadFromJson(self.json())
        return c

    def loadFromJson(self, json):
        if not json:
            return self
        self.slotType = Slot().loadFromJson(json.get('slotType'))
        self.concrete = Slot().loadFromJson(json.get('concrete'))
        self.instanced = Slot().loadFromJson(json.get('instanced'))
        self.human = Human().loadFromJson(json.get('human'))
        return self

    def json(self, skipTypes = False):
        d = { }
        if not skipTypes:
            d["type"] = self.typeName
        if self.slotType != None: d['slotType'] = self.slotType.json(skipTypes = skipTypes) if hasattr(self.slotType, 'json') else id(self.slotType)
        if self.concrete != None: d['concrete'] = self.concrete.json(skipTypes = skipTypes) if hasattr(self.concrete, 'json') else id(self.concrete)
        if self.instanced != None: d['instanced'] = self.instanced.json(skipTypes = skipTypes) if hasattr(self.instanced, 'json') else id(self.instanced)
        if self.human != None: d['human'] = self.human.json(skipTypes = skipTypes) if hasattr(self.human, 'json') else id(self.human)
        return d

class MetaSlex(object):

    def __init__(self, op = None, args = None):
        self.op = op or None  # type MetaSlot
        self.args = args or []  # type [MetaSlot]

    @property
    def typeName(self):
        return "MetaSlex"

    @property
    def fsType(self):
        return fs.MetaSlex

    def defaultDict(self):
        return {
            'op' : self.op or None,
            'args' : self.args or [],
        }

    def _description(self):
        return "MetaSlex: `{}`".format(", ".join([ "{}={}".format(k, v) for k, v in self.json(skipTypes = True).items() ]))

    def _newObjectOfSameType(self):
        return MetaSlex()

    def clone(self):
        c = self._newObjectOfSameType()
        if hasattr(self, 'serialize'):
            c.deserialize(self.serialize())
        else:
            c.loadFromJson(self.json())
        return c

    def loadFromJson(self, json):
        if not json:
            return self
        self.op = MetaSlot().loadFromJson(json.get('op'))
        self.args = [ MetaSlot().loadFromJson(x) for x in json.get('args') or [] ]
        return self

    def json(self, skipTypes = False):
        d = { }
        if not skipTypes:
            d["type"] = self.typeName
        if self.op != None: d['op'] = self.op.json(skipTypes = skipTypes) if hasattr(self.op, 'json') else id(self.op)
        if self.args != None: d['args'] = [ x.json(skipTypes = skipTypes) for x in self.args ]
        return d

class SlopDef(object):

    def __init__(self, params = None, locals = None, steps = None):
        self.params = params or []  # type [SlotDef]
        self.locals = locals or []  # type [SlotDef]
        self.steps = steps or []  # type [SlexDef]

    @property
    def typeName(self):
        return "SlopDef"

    @property
    def fsType(self):
        return fs.SlopDef

    def defaultDict(self):
        return {
            'params' : self.params or [],
            'locals' : self.locals or [],
            'steps' : self.steps or [],
        }

    def _description(self):
        return "SlopDef: `{}`".format(", ".join([ "{}={}".format(k, v) for k, v in self.json(skipTypes = True).items() ]))

    def _newObjectOfSameType(self):
        return SlopDef()

    def clone(self):
        c = self._newObjectOfSameType()
        if hasattr(self, 'serialize'):
            c.deserialize(self.serialize())
        else:
            c.loadFromJson(self.json())
        return c

    def loadFromJson(self, json):
        if not json:
            return self
        self.params = [ SlotDef().loadFromJson(x) for x in json.get('params') or [] ]
        self.locals = [ SlotDef().loadFromJson(x) for x in json.get('locals') or [] ]
        self.steps = [ SlexDef().loadFromJson(x) for x in json.get('steps') or [] ]
        return self

    def json(self, skipTypes = False):
        d = { }
        if not skipTypes:
            d["type"] = self.typeName
        if self.params != None: d['params'] = [ x.json(skipTypes = skipTypes) for x in self.params ]
        if self.locals != None: d['locals'] = [ x.json(skipTypes = skipTypes) for x in self.locals ]
        if self.steps != None: d['steps'] = [ x.json(skipTypes = skipTypes) for x in self.steps ]
        return d

class SlotRef(object):

    def __init__(self, name = None, slot = None):
        self.name = name or ''  # type String
        self.slot = slot or None  # type SlotDef

    @property
    def typeName(self):
        return "SlotRef"

    @property
    def fsType(self):
        return fs.SlotRef

    def defaultDict(self):
        return {
            'name' : self.name or '',
            'slot' : self.slot or None,
        }

    def _description(self):
        return "SlotRef: `{}`".format(", ".join([ "{}={}".format(k, v) for k, v in self.json(skipTypes = True).items() ]))

    def _newObjectOfSameType(self):
        return SlotRef()

    def clone(self):
        c = self._newObjectOfSameType()
        if hasattr(self, 'serialize'):
            c.deserialize(self.serialize())
        else:
            c.loadFromJson(self.json())
        return c

    def loadFromJson(self, json):
        if not json:
            return self
        self.name = json.get('name')
        self.slot = SlotDef().loadFromJson(json.get('slot'))
        return self

    def json(self, skipTypes = False):
        d = { }
        if not skipTypes:
            d["type"] = self.typeName
        if self.name != None: d['name'] = self.name
        if self.slot != None: d['slot'] = self.slot.json(skipTypes = skipTypes) if hasattr(self.slot, 'json') else id(self.slot)
        return d

class SlotDef(object):

    def __init__(self, name = None, slotType = None, constant = None, slop = None, linked = None):
        self.name = name or ''  # type String
        self.slotType = slotType or ''  # type String
        self.constant = constant or None  # type Object
        self.slop = slop or None  # type SlopDef
        self.linked = linked or None  # type MetaSlot

    @property
    def typeName(self):
        return "SlotDef"

    @property
    def fsType(self):
        return fs.SlotDef

    def defaultDict(self):
        return {
            'name' : self.name or '',
            'slotType' : self.slotType or '',
            'constant' : self.constant or None,
            'slop' : self.slop or None,
            'linked' : self.linked or None,
        }

    def _description(self):
        return "SlotDef: `{}`".format(", ".join([ "{}={}".format(k, v) for k, v in self.json(skipTypes = True).items() ]))

    def _newObjectOfSameType(self):
        return SlotDef()

    def clone(self):
        c = self._newObjectOfSameType()
        if hasattr(self, 'serialize'):
            c.deserialize(self.serialize())
        else:
            c.loadFromJson(self.json())
        return c

    def loadFromJson(self, json):
        if not json:
            return self
        self.name = json.get('name')
        self.slotType = json.get('slotType')
        self.constant = Object().loadFromJson(json.get('constant'))
        self.slop = SlopDef().loadFromJson(json.get('slop'))
        self.linked = MetaSlot().loadFromJson(json.get('linked'))
        return self

    def json(self, skipTypes = False):
        d = { }
        if not skipTypes:
            d["type"] = self.typeName
        if self.name != None: d['name'] = self.name
        if self.slotType != None: d['slotType'] = self.slotType
        if self.constant != None: d['constant'] = self.constant.json(skipTypes = skipTypes) if hasattr(self.constant, 'json') else id(self.constant)
        if self.slop != None: d['slop'] = self.slop.json(skipTypes = skipTypes) if hasattr(self.slop, 'json') else id(self.slop)
        if self.linked != None: d['linked'] = self.linked.json(skipTypes = skipTypes) if hasattr(self.linked, 'json') else id(self.linked)
        return d

class SlexDef(object):

    def __init__(self, op = None, args = None):
        self.op = op or None  # type SlotRef
        self.args = args or []  # type [SlotRef]

    @property
    def typeName(self):
        return "SlexDef"

    @property
    def fsType(self):
        return fs.SlexDef

    def defaultDict(self):
        return {
            'op' : self.op or None,
            'args' : self.args or [],
        }

    def _description(self):
        return "SlexDef: `{}`".format(", ".join([ "{}={}".format(k, v) for k, v in self.json(skipTypes = True).items() ]))

    def _newObjectOfSameType(self):
        return SlexDef()

    def clone(self):
        c = self._newObjectOfSameType()
        if hasattr(self, 'serialize'):
            c.deserialize(self.serialize())
        else:
            c.loadFromJson(self.json())
        return c

    def loadFromJson(self, json):
        if not json:
            return self
        self.op = SlotRef().loadFromJson(json.get('op'))
        self.args = [ SlotRef().loadFromJson(x) for x in json.get('args') or [] ]
        return self

    def json(self, skipTypes = False):
        d = { }
        if not skipTypes:
            d["type"] = self.typeName
        if self.op != None: d['op'] = self.op.json(skipTypes = skipTypes) if hasattr(self.op, 'json') else id(self.op)
        if self.args != None: d['args'] = [ x.json(skipTypes = skipTypes) for x in self.args ]
        return d

class Human(object):

    def __init__(self, name = None, displayType = None):
        self.name = name or ''  # type String
        self.displayType = displayType or ''  # type String

    @property
    def typeName(self):
        return "Human"

    @property
    def fsType(self):
        return fs.Human

    def defaultDict(self):
        return {
            'name' : self.name or '',
            'displayType' : self.displayType or '',
        }

    def _description(self):
        return "Human: `{}`".format(", ".join([ "{}={}".format(k, v) for k, v in self.json(skipTypes = True).items() ]))

    def _newObjectOfSameType(self):
        return Human()

    def clone(self):
        c = self._newObjectOfSameType()
        if hasattr(self, 'serialize'):
            c.deserialize(self.serialize())
        else:
            c.loadFromJson(self.json())
        return c

    def loadFromJson(self, json):
        if not json:
            return self
        self.name = json.get('name')
        self.displayType = json.get('displayType')
        return self

    def json(self, skipTypes = False):
        d = { }
        if not skipTypes:
            d["type"] = self.typeName
        if self.name != None: d['name'] = self.name
        if self.displayType != None: d['displayType'] = self.displayType
        return d


def newObjectOfType(type):
    return globals()[type]()

_g_fsMap = {
    fs.ExecutionContext : ExecutionContext,
    fs.ExecutionNode : ExecutionNode,
    fs.SlotType : SlotType,
    fs.Slot : Slot,
    fs.Slex : Slex,
    fs.Slop : Slop,
    fs.MetaSlop : MetaSlop,
    fs.MetaSlot : MetaSlot,
    fs.MetaSlex : MetaSlex,
    fs.SlopDef : SlopDef,
    fs.SlotRef : SlotRef,
    fs.SlotDef : SlotDef,
    fs.SlexDef : SlexDef,
    fs.Human : Human,
}

def newObjectOfFixedStringType(type):
    return _g_fsMap[type]()

def hasObjectOfFixedStringType(type):
    return type in _g_fsMap

def objectFromJson(j):
    return newObjectOfType(j['type']).loadFromJson(j)
