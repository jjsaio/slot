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

    def __init__(self, do = None, executed = None, next = None, parent = None):
        self.do = do or None  # type Do
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
            'do' : self.do or None,
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
        self.do = Do().loadFromJson(json.get('do'))
        self.executed = json.get('executed')
        self.next = ExecutionNode().loadFromJson(json.get('next'))
        self.parent = ExecutionNode().loadFromJson(json.get('parent'))
        return self

    def json(self, skipTypes = False):
        d = { }
        if not skipTypes:
            d["type"] = self.typeName
        if self.do != None: d['do'] = self.do.json(skipTypes = skipTypes) if hasattr(self.do, 'json') else id(self.do)
        if self.executed != None: d['executed'] = self.executed
        if self.next != None: d['next'] = self.next.json(skipTypes = skipTypes) if hasattr(self.next, 'json') else id(self.next)
        if self.parent != None: d['parent'] = self.parent.json(skipTypes = skipTypes) if hasattr(self.parent, 'json') else id(self.parent)
        return d

class CellType(object):

    def __init__(self, nativeType = None, human = None):
        self.nativeType = nativeType or None  # type Object
        self.human = human or None  # type Human

    @property
    def typeName(self):
        return "CellType"

    @property
    def fsType(self):
        return fs.CellType

    def defaultDict(self):
        return {
            'nativeType' : self.nativeType or None,
            'human' : self.human or None,
        }

    def _description(self):
        return "CellType: `{}`".format(", ".join([ "{}={}".format(k, v) for k, v in self.json(skipTypes = True).items() ]))

    def _newObjectOfSameType(self):
        return CellType()

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

class Cell(object):

    def __init__(self, cellType = None, data = None, human = None):
        self.cellType = cellType or None  # type CellType
        self.data = data or None  # type Pointer
        self.human = human or None  # type Human

    @property
    def typeName(self):
        return "Cell"

    @property
    def fsType(self):
        return fs.Cell

    def defaultDict(self):
        return {
            'cellType' : self.cellType or None,
            'data' : self.data or None,
            'human' : self.human or None,
        }

    def _description(self):
        return "Cell: `{}`".format(", ".join([ "{}={}".format(k, v) for k, v in self.json(skipTypes = True).items() ]))

    def _newObjectOfSameType(self):
        return Cell()

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
        self.cellType = CellType().loadFromJson(json.get('cellType'))
        self.data = json.get('data')
        self.human = Human().loadFromJson(json.get('human'))
        return self

    def json(self, skipTypes = False):
        d = { }
        if not skipTypes:
            d["type"] = self.typeName
        if self.cellType != None: d['cellType'] = self.cellType.json(skipTypes = skipTypes) if hasattr(self.cellType, 'json') else id(self.cellType)
        if self.data != None: d['data'] = id(self.data)
        if self.human != None: d['human'] = self.human.json(skipTypes = skipTypes) if hasattr(self.human, 'json') else id(self.human)
        return d

class Do(object):

    def __init__(self, op = None, args = None):
        self.op = op or None  # type Cop
        self.args = args or []  # type [Cell]

    @property
    def typeName(self):
        return "Do"

    @property
    def fsType(self):
        return fs.Do

    def defaultDict(self):
        return {
            'op' : self.op or None,
            'args' : self.args or [],
        }

    def _description(self):
        return "Do: `{}`".format(", ".join([ "{}={}".format(k, v) for k, v in self.json(skipTypes = True).items() ]))

    def _newObjectOfSameType(self):
        return Do()

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
        self.op = Cop().loadFromJson(json.get('op'))
        self.args = [ Cell().loadFromJson(x) for x in json.get('args') or [] ]
        return self

    def json(self, skipTypes = False):
        d = { }
        if not skipTypes:
            d["type"] = self.typeName
        if self.op != None: d['op'] = self.op.json(skipTypes = skipTypes) if hasattr(self.op, 'json') else id(self.op)
        if self.args != None: d['args'] = [ x.json(skipTypes = skipTypes) for x in self.args ]
        return d

class Cop(object):

    def __init__(self, op = None, captured = None):
        self.op = op or None  # type MetaCop
        self.captured = captured or []  # type [Cell]

    @property
    def typeName(self):
        return "Cop"

    @property
    def fsType(self):
        return fs.Cop

    def defaultDict(self):
        return {
            'op' : self.op or None,
            'captured' : self.captured or [],
        }

    def _description(self):
        return "Cop: `{}`".format(", ".join([ "{}={}".format(k, v) for k, v in self.json(skipTypes = True).items() ]))

    def _newObjectOfSameType(self):
        return Cop()

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
        self.op = MetaCop().loadFromJson(json.get('op'))
        self.captured = [ Cell().loadFromJson(x) for x in json.get('captured') or [] ]
        return self

    def json(self, skipTypes = False):
        d = { }
        if not skipTypes:
            d["type"] = self.typeName
        if self.op != None: d['op'] = self.op.json(skipTypes = skipTypes) if hasattr(self.op, 'json') else id(self.op)
        if self.captured != None: d['captured'] = [ x.json(skipTypes = skipTypes) for x in self.captured ]
        return d

class MetaCop(object):

    def __init__(self, params = None, captured = None, locals = None, steps = None, native = None, human = None):
        self.params = params or []  # type [MetaCell]
        self.captured = captured or []  # type [MetaCell]
        self.locals = locals or []  # type [MetaCell]
        self.steps = steps or []  # type [MetaDo]
        self.native = native or None  # type Object
        self.human = human or None  # type Human

    @property
    def typeName(self):
        return "MetaCop"

    @property
    def fsType(self):
        return fs.MetaCop

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
        return "MetaCop: `{}`".format(", ".join([ "{}={}".format(k, v) for k, v in self.json(skipTypes = True).items() ]))

    def _newObjectOfSameType(self):
        return MetaCop()

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
        self.params = [ MetaCell().loadFromJson(x) for x in json.get('params') or [] ]
        self.captured = [ MetaCell().loadFromJson(x) for x in json.get('captured') or [] ]
        self.locals = [ MetaCell().loadFromJson(x) for x in json.get('locals') or [] ]
        self.steps = [ MetaDo().loadFromJson(x) for x in json.get('steps') or [] ]
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

class MetaCell(object):

    def __init__(self, cellType = None, concrete = None, instanced = None, human = None):
        self.cellType = cellType or None  # type Cell
        self.concrete = concrete or None  # type Cell
        self.instanced = instanced or None  # type Cell
        self.human = human or None  # type Human

    @property
    def typeName(self):
        return "MetaCell"

    @property
    def fsType(self):
        return fs.MetaCell

    def defaultDict(self):
        return {
            'cellType' : self.cellType or None,
            'concrete' : self.concrete or None,
            'instanced' : self.instanced or None,
            'human' : self.human or None,
        }

    def _description(self):
        return "MetaCell: `{}`".format(", ".join([ "{}={}".format(k, v) for k, v in self.json(skipTypes = True).items() ]))

    def _newObjectOfSameType(self):
        return MetaCell()

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
        self.cellType = Cell().loadFromJson(json.get('cellType'))
        self.concrete = Cell().loadFromJson(json.get('concrete'))
        self.instanced = Cell().loadFromJson(json.get('instanced'))
        self.human = Human().loadFromJson(json.get('human'))
        return self

    def json(self, skipTypes = False):
        d = { }
        if not skipTypes:
            d["type"] = self.typeName
        if self.cellType != None: d['cellType'] = self.cellType.json(skipTypes = skipTypes) if hasattr(self.cellType, 'json') else id(self.cellType)
        if self.concrete != None: d['concrete'] = self.concrete.json(skipTypes = skipTypes) if hasattr(self.concrete, 'json') else id(self.concrete)
        if self.instanced != None: d['instanced'] = self.instanced.json(skipTypes = skipTypes) if hasattr(self.instanced, 'json') else id(self.instanced)
        if self.human != None: d['human'] = self.human.json(skipTypes = skipTypes) if hasattr(self.human, 'json') else id(self.human)
        return d

class MetaDo(object):

    def __init__(self, op = None, args = None):
        self.op = op or None  # type MetaCell
        self.args = args or []  # type [MetaCell]

    @property
    def typeName(self):
        return "MetaDo"

    @property
    def fsType(self):
        return fs.MetaDo

    def defaultDict(self):
        return {
            'op' : self.op or None,
            'args' : self.args or [],
        }

    def _description(self):
        return "MetaDo: `{}`".format(", ".join([ "{}={}".format(k, v) for k, v in self.json(skipTypes = True).items() ]))

    def _newObjectOfSameType(self):
        return MetaDo()

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
        self.op = MetaCell().loadFromJson(json.get('op'))
        self.args = [ MetaCell().loadFromJson(x) for x in json.get('args') or [] ]
        return self

    def json(self, skipTypes = False):
        d = { }
        if not skipTypes:
            d["type"] = self.typeName
        if self.op != None: d['op'] = self.op.json(skipTypes = skipTypes) if hasattr(self.op, 'json') else id(self.op)
        if self.args != None: d['args'] = [ x.json(skipTypes = skipTypes) for x in self.args ]
        return d

class CopDef(object):

    def __init__(self, params = None, locals = None, steps = None):
        self.params = params or []  # type [CellDef]
        self.locals = locals or []  # type [CellDef]
        self.steps = steps or []  # type [DoDef]

    @property
    def typeName(self):
        return "CopDef"

    @property
    def fsType(self):
        return fs.CopDef

    def defaultDict(self):
        return {
            'params' : self.params or [],
            'locals' : self.locals or [],
            'steps' : self.steps or [],
        }

    def _description(self):
        return "CopDef: `{}`".format(", ".join([ "{}={}".format(k, v) for k, v in self.json(skipTypes = True).items() ]))

    def _newObjectOfSameType(self):
        return CopDef()

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
        self.params = [ CellDef().loadFromJson(x) for x in json.get('params') or [] ]
        self.locals = [ CellDef().loadFromJson(x) for x in json.get('locals') or [] ]
        self.steps = [ DoDef().loadFromJson(x) for x in json.get('steps') or [] ]
        return self

    def json(self, skipTypes = False):
        d = { }
        if not skipTypes:
            d["type"] = self.typeName
        if self.params != None: d['params'] = [ x.json(skipTypes = skipTypes) for x in self.params ]
        if self.locals != None: d['locals'] = [ x.json(skipTypes = skipTypes) for x in self.locals ]
        if self.steps != None: d['steps'] = [ x.json(skipTypes = skipTypes) for x in self.steps ]
        return d

class CellRef(object):

    def __init__(self, name = None, cell = None):
        self.name = name or ''  # type String
        self.cell = cell or None  # type CellDef

    @property
    def typeName(self):
        return "CellRef"

    @property
    def fsType(self):
        return fs.CellRef

    def defaultDict(self):
        return {
            'name' : self.name or '',
            'cell' : self.cell or None,
        }

    def _description(self):
        return "CellRef: `{}`".format(", ".join([ "{}={}".format(k, v) for k, v in self.json(skipTypes = True).items() ]))

    def _newObjectOfSameType(self):
        return CellRef()

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
        self.cell = CellDef().loadFromJson(json.get('cell'))
        return self

    def json(self, skipTypes = False):
        d = { }
        if not skipTypes:
            d["type"] = self.typeName
        if self.name != None: d['name'] = self.name
        if self.cell != None: d['cell'] = self.cell.json(skipTypes = skipTypes) if hasattr(self.cell, 'json') else id(self.cell)
        return d

class CellDef(object):

    def __init__(self, name = None, cellType = None, constant = None, cop = None, linked = None):
        self.name = name or ''  # type String
        self.cellType = cellType or ''  # type String
        self.constant = constant or None  # type Object
        self.cop = cop or None  # type CopDef
        self.linked = linked or None  # type MetaCell

    @property
    def typeName(self):
        return "CellDef"

    @property
    def fsType(self):
        return fs.CellDef

    def defaultDict(self):
        return {
            'name' : self.name or '',
            'cellType' : self.cellType or '',
            'constant' : self.constant or None,
            'cop' : self.cop or None,
            'linked' : self.linked or None,
        }

    def _description(self):
        return "CellDef: `{}`".format(", ".join([ "{}={}".format(k, v) for k, v in self.json(skipTypes = True).items() ]))

    def _newObjectOfSameType(self):
        return CellDef()

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
        self.cellType = json.get('cellType')
        self.constant = Object().loadFromJson(json.get('constant'))
        self.cop = CopDef().loadFromJson(json.get('cop'))
        self.linked = MetaCell().loadFromJson(json.get('linked'))
        return self

    def json(self, skipTypes = False):
        d = { }
        if not skipTypes:
            d["type"] = self.typeName
        if self.name != None: d['name'] = self.name
        if self.cellType != None: d['cellType'] = self.cellType
        if self.constant != None: d['constant'] = self.constant.json(skipTypes = skipTypes) if hasattr(self.constant, 'json') else id(self.constant)
        if self.cop != None: d['cop'] = self.cop.json(skipTypes = skipTypes) if hasattr(self.cop, 'json') else id(self.cop)
        if self.linked != None: d['linked'] = self.linked.json(skipTypes = skipTypes) if hasattr(self.linked, 'json') else id(self.linked)
        return d

class DoDef(object):

    def __init__(self, op = None, args = None):
        self.op = op or None  # type CellRef
        self.args = args or []  # type [CellRef]

    @property
    def typeName(self):
        return "DoDef"

    @property
    def fsType(self):
        return fs.DoDef

    def defaultDict(self):
        return {
            'op' : self.op or None,
            'args' : self.args or [],
        }

    def _description(self):
        return "DoDef: `{}`".format(", ".join([ "{}={}".format(k, v) for k, v in self.json(skipTypes = True).items() ]))

    def _newObjectOfSameType(self):
        return DoDef()

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
        self.op = CellRef().loadFromJson(json.get('op'))
        self.args = [ CellRef().loadFromJson(x) for x in json.get('args') or [] ]
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
    fs.CellType : CellType,
    fs.Cell : Cell,
    fs.Do : Do,
    fs.Cop : Cop,
    fs.MetaCop : MetaCop,
    fs.MetaCell : MetaCell,
    fs.MetaDo : MetaDo,
    fs.CopDef : CopDef,
    fs.CellRef : CellRef,
    fs.CellDef : CellDef,
    fs.DoDef : DoDef,
    fs.Human : Human,
}

def newObjectOfFixedStringType(type):
    return _g_fsMap[type]()

def hasObjectOfFixedStringType(type):
    return type in _g_fsMap

def objectFromJson(j):
    return newObjectOfType(j['type']).loadFromJson(j)
