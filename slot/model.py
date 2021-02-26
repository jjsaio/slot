import sys

from .fs import fs


class Slot(object):

    def __init__(self, type = None, data = None, subslots = None, human = None):
        self.type = type or None  # type Slot
        self.data = data or None  # type Object
        self.subslots = subslots or []  # type [Slot]
        self.human = human or None  # type Human

    @property
    def typeName(self):
        return "Slot"

    @property
    def fsType(self):
        return fs.Slot

    def defaultDict(self):
        return {
            'type' : self.type or None,
            'data' : self.data or None,
            'subslots' : self.subslots or [],
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
        self.type = Slot().loadFromJson(json.get('type'))
        self.data = Object().loadFromJson(json.get('data'))
        self.subslots = [ Slot().loadFromJson(x) for x in json.get('subslots') or [] ]
        self.human = Human().loadFromJson(json.get('human'))
        return self

    def json(self, skipTypes = False):
        d = { }
        if not skipTypes:
            d["type"] = self.typeName
        if self.type != None: d['type'] = self.type.json(skipTypes = skipTypes) if hasattr(self.type, 'json') else id(self.type)
        if self.data != None: d['data'] = self.data.json(skipTypes = skipTypes) if hasattr(self.data, 'json') else id(self.data)
        if self.subslots != None: d['subslots'] = [ x.json(skipTypes = skipTypes) for x in self.subslots ]
        if self.human != None: d['human'] = self.human.json(skipTypes = skipTypes) if hasattr(self.human, 'json') else id(self.human)
        return d

class SlotRef(object):

    def __init__(self, name = None):
        self.name = name or ''  # type String

    @property
    def typeName(self):
        return "SlotRef"

    @property
    def fsType(self):
        return fs.SlotRef

    def defaultDict(self):
        return {
            'name' : self.name or '',
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
        return self

    def json(self, skipTypes = False):
        d = { }
        if not skipTypes:
            d["type"] = self.typeName
        if self.name != None: d['name'] = self.name
        return d

class Slop(object):

    def __init__(self, params = None, locals = None, steps = None, native = None, human = None):
        self.params = params or []  # type [MetaSlot]
        self.locals = locals or []  # type [MetaSlot]
        self.steps = steps or []  # type [MetaSlex]
        self.native = native or None  # type Object
        self.human = human or None  # type Human

    @property
    def typeName(self):
        return "Slop"

    @property
    def fsType(self):
        return fs.Slop

    def defaultDict(self):
        return {
            'params' : self.params or [],
            'locals' : self.locals or [],
            'steps' : self.steps or [],
            'native' : self.native or None,
            'human' : self.human or None,
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
        self.params = [ MetaSlot().loadFromJson(x) for x in json.get('params') or [] ]
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
        if self.locals != None: d['locals'] = [ x.json(skipTypes = skipTypes) for x in self.locals ]
        if self.steps != None: d['steps'] = [ x.json(skipTypes = skipTypes) for x in self.steps ]
        if self.native != None: d['native'] = self.native.json(skipTypes = skipTypes) if hasattr(self.native, 'json') else id(self.native)
        if self.human != None: d['human'] = self.human.json(skipTypes = skipTypes) if hasattr(self.human, 'json') else id(self.human)
        return d

class Slex(object):

    def __init__(self, op = None, args = None, human = None):
        self.op = op or None  # type Slot
        self.args = args or []  # type [Slot]
        self.human = human or None  # type Human

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
            'human' : self.human or None,
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
        self.op = Slot().loadFromJson(json.get('op'))
        self.args = [ Slot().loadFromJson(x) for x in json.get('args') or [] ]
        self.human = Human().loadFromJson(json.get('human'))
        return self

    def json(self, skipTypes = False):
        d = { }
        if not skipTypes:
            d["type"] = self.typeName
        if self.op != None: d['op'] = self.op.json(skipTypes = skipTypes) if hasattr(self.op, 'json') else id(self.op)
        if self.args != None: d['args'] = [ x.json(skipTypes = skipTypes) for x in self.args ]
        if self.human != None: d['human'] = self.human.json(skipTypes = skipTypes) if hasattr(self.human, 'json') else id(self.human)
        return d

class MetaSlot(object):

    def __init__(self, type = None, concrete = None, instanced = None, human = None):
        self.type = type or None  # type Slot
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
            'type' : self.type or None,
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
        self.type = Slot().loadFromJson(json.get('type'))
        self.concrete = Slot().loadFromJson(json.get('concrete'))
        self.instanced = Slot().loadFromJson(json.get('instanced'))
        self.human = Human().loadFromJson(json.get('human'))
        return self

    def json(self, skipTypes = False):
        d = { }
        if not skipTypes:
            d["type"] = self.typeName
        if self.type != None: d['type'] = self.type.json(skipTypes = skipTypes) if hasattr(self.type, 'json') else id(self.type)
        if self.concrete != None: d['concrete'] = self.concrete.json(skipTypes = skipTypes) if hasattr(self.concrete, 'json') else id(self.concrete)
        if self.instanced != None: d['instanced'] = self.instanced.json(skipTypes = skipTypes) if hasattr(self.instanced, 'json') else id(self.instanced)
        if self.human != None: d['human'] = self.human.json(skipTypes = skipTypes) if hasattr(self.human, 'json') else id(self.human)
        return d

class MetaSlex(object):

    def __init__(self, op = None, args = None, human = None):
        self.op = op or None  # type MetaSlot
        self.args = args or []  # type [MetaSlot]
        self.human = human or None  # type Human

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
            'human' : self.human or None,
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
        self.human = Human().loadFromJson(json.get('human'))
        return self

    def json(self, skipTypes = False):
        d = { }
        if not skipTypes:
            d["type"] = self.typeName
        if self.op != None: d['op'] = self.op.json(skipTypes = skipTypes) if hasattr(self.op, 'json') else id(self.op)
        if self.args != None: d['args'] = [ x.json(skipTypes = skipTypes) for x in self.args ]
        if self.human != None: d['human'] = self.human.json(skipTypes = skipTypes) if hasattr(self.human, 'json') else id(self.human)
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

class Command(object):

    def __init__(self, key = None, data = None):
        self.key = key or ''  # type String
        self.data = data or None  # type Object

    @property
    def typeName(self):
        return "Command"

    @property
    def fsType(self):
        return fs.Command

    def defaultDict(self):
        return {
            'key' : self.key or '',
            'data' : self.data or None,
        }

    def _description(self):
        return "Command: `{}`".format(", ".join([ "{}={}".format(k, v) for k, v in self.json(skipTypes = True).items() ]))

    def _newObjectOfSameType(self):
        return Command()

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
        self.key = json.get('key')
        self.data = Object().loadFromJson(json.get('data'))
        return self

    def json(self, skipTypes = False):
        d = { }
        if not skipTypes:
            d["type"] = self.typeName
        if self.key != None: d['key'] = self.key
        if self.data != None: d['data'] = self.data.json(skipTypes = skipTypes) if hasattr(self.data, 'json') else id(self.data)
        return d


def newObjectOfType(type):
    return globals()[type]()

_g_fsMap = {
    fs.Slot : Slot,
    fs.SlotRef : SlotRef,
    fs.Slop : Slop,
    fs.Slex : Slex,
    fs.MetaSlot : MetaSlot,
    fs.MetaSlex : MetaSlex,
    fs.Human : Human,
    fs.Command : Command,
}

def newObjectOfFixedStringType(type):
    return _g_fsMap[type]()

def hasObjectOfFixedStringType(type):
    return type in _g_fsMap

def objectFromJson(j):
    return newObjectOfType(j['type']).loadFromJson(j)
