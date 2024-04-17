# pylint: disable=[W,R,C,import-error]

from Location import Location
from Identifier import Identifier
from EngineErrors import IdentifierError, InvalidObjectError
from Interactable import Interactable
from FunctionMemory import FunctionMemory
from EngineOperation import _EngineOperation
from Logger import Log
from Util import Util
from Loader import Loader
from Serializer import Serializer, Serializable

from typing import Any

import re, glob, json

@Serializable("AbstractInteractable")
class AbstractInteractable:
    _loaded = {}
    _link_parents = []
    
    def __init__(self, identifier:Identifier, data:dict):
        self.identifier = identifier
        self._raw_data = data
        self.children: list[AbstractInteractable] = []
        self.parent: AbstractInteractable|None = None

        self.fields: dict[str, dict[str, Any]] = data.get("fields", {})
        self.data: dict[str, Any] = data.get("data", {})
        self.interaction: dict = data.get("interaction", {})

    def _set_parent(self, parent):
        self.parent = parent
        parent.children.append(self)

    def is_parent_of(self, other):
        p = other
        while p is not None:
            if self == p:
                return True
            p = p.parent
        return False
    
    def inherets_from(self, other):
        p = self
        while p is not None:
            if p == other:
                return True
            p = p.parent
        return False

    def get_children(self, depth:int=-1): # recursive way to get a flat list of all sub children to some depth
        children = []
        for child in self.children:
            if not child.is_template:
                children.append(child)
            if depth != 0:
                children += child.get_children(depth-1)
        return children

    def get_parent_chain(self):
        if self.parent is None:
            return []
        else:
            return [self.parent] + self.parent.get_parent_chain()

    def getFieldValues(self, function_memory:FunctionMemory, values:dict):
        vals = {}
        for field_name, field_data in self.fields.items():

            field_data: dict
            val = {}
            if (_type := field_data.get("type", None)) is not None:

                if _type not in function_memory.data_types:
                    raise InvalidObjectError(f"Interactable field '{field_name}' has type '{_type}' which does not exist")
                
                allowed = function_memory.engine.loader.loader_function.getRelatedFunctionNames(_type)

                allowed += [
                    "engine:math/",
                    "engine:logic/",
                    "engine:random/"
                ]
                disallowed = [
                    "engine:player/get_input"
                ]
                value = values.get(field_name, field_data.get("default", None))
                if value is None and field_data.get("required", False) is True:
                    raise InvalidObjectError(f"Interactable field '{field_name}' is required, but has no value")

                if function_memory.engine.loader.scanFunction(function_memory, value, allowed, disallowed):
                    ev = function_memory.generatorEvaluateFunction(value)
                    v = None
                    try:
                        while True:
                            v = ev.send(None)
                            if isinstance(v, _EngineOperation):
                                raise InvalidObjectError(f"Interactable field '{field_name}' cannot contain functions that use Engine Operations")
                    except StopIteration as e:
                        v = e.value or v
                    vals.update({field_name: {"type": _type, "value": v}})
                else:
                    raise InvalidObjectError(f"Interactable field '{field_name}' value is invalid ({value})")

            else:
                raise InvalidObjectError(f"Interactable field '{field_name}' has no 'type' specified")
        vals.update({"id": values.get("id")})
        return vals

    def createInstance(self, function_memory:FunctionMemory, field_values):
        return Interactable(self,
            self.interaction,
            self.getFieldValues(function_memory, field_values),
            Util.deepCopy(self.data)
        )

    @classmethod
    def createInteractable(cls, function_memory:FunctionMemory, data:dict):
        
        interaction_type = data.get("type", None)
        if interaction_type is None:
            raise InvalidObjectError(f"Interaction has no specified type! (data: {data})")
        

        interaction_id = data.get("id", None)
        if interaction_id is None:
            raise InvalidObjectError(f"Interaction has no id! (data: {data})")
        data.pop("type")
        #data.pop("id")

        if (abstract := cls._loaded.get(interaction_type, None)) is not None:
            abstract: AbstractInteractable
            return abstract.createInstance(function_memory, data)
        else:
            raise InvalidObjectError(f"Interaction type '{interaction_type}' does not exist! (id: {interaction_id})")

    @classmethod
    def loadData(cls, engine) -> dict:
        files: list[str] = glob.glob("**/interactable/*.json", recursive=True)

        Log["loadup"]["abstract"]["interactable"](f"found {len(files)} interactable file{'s' if len(files) != 1 else ''}")
        for file in files:
            file: str
            Log["loadup"]["abstract"]["interactable"](f"loading AbstractInteractable from '{file}'")
            data = Loader.load(file)
            
            Id = Identifier.fromFile(file)
            cls._loaded.update({Id.full(): cls(Id, data)})

        Log["loadup"]["abstract"]["interactable"]("linking AbstractInteractable parents...")
        for a, p in cls._link_parents:
            a: AbstractInteractable
            p: str
            if parent := cls._loaded.get(p, None):
                if parent is a:
                    Log["ERROR"]["loadup"]["abstract"]["interactable"]("cannot set object as it's own parent")
                    continue
                elif parent in a.get_parent_chain():
                    Log["ERROR"]["loadup"]["abstract"]["interactable"]("circular parent loop found")
                    continue
                a._set_parent(parent)
            else:
                Log["ERROR"]["loadup"]["abstract"]["interactable"](f"parent does not exist: '{p}'")
        
        Log["loadup"]["abstract"]["interactable"]("verifying AbstractInteractable completion...")
        Log.track(len(cls._loaded), "loadup", "abstract", "interactable")
        for l, o in cls._loaded.copy().items():
            l: str
            o: AbstractInteractable
            try:
                #o.getFieldValues(engine._function_memory)
                Log.success()
            except InvalidObjectError:
                e: AbstractInteractable = cls._loaded.pop(l)
                Log.ERROR("loadup", "abstract", "interactable", f"failed to load interactable: {e.identifier}")

        Log.end_track()

        cls._link_parents.clear()

        Log["loadup"]["abstract"]["interactable"]("AbstractInteractable loading complete")
        return cls._loaded

    def serialize(self):
        return {
            "identifier": Serializer.serialize(self.identifier),
            "_raw_data": Serializer.serialize(self._raw_data),
            "children": Serializer.serialize(self.children),
            "parent": Serializer.serialize(self.parent),
            "fields": Serializer.serialize(self.fields),
            "data": Serializer.serialize(self.data),
            "interaction": Serializer.serialize(self.interaction)
        }

    @classmethod
    def deserialize(cls, instance, data:dict):
        Serializer.smartDeserialize(instance, data)

