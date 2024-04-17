# pylint: disable=[W,R,C,import-error]

from GameObject import GameObject
from Identifier import Identifier
from DynamicValue import DynamicValue
from FunctionalElement import FunctionalElement
from FunctionMemory import FunctionMemory
from Player import Player
from EngineOperation import _EngineOperation
from Serializer import Serializer, Serializable

from typing import Any

@Serializable("Interactable")
class Interactable(FunctionalElement):

    def __init__(self, abstract, interaction_event, field_values:dict, data:dict):
        self.abstract = abstract
        self.field_values = field_values
        self.interaction_event = interaction_event
        self.data = data
        self.name = self.field_values.pop("id")

    def serialize(self):
        return {
            "abstract": Serializer.serialize(self.abstract),
            "field_values": Serializer.serialize(self.field_values),
            "interaction_event": Serializer.serialize(self.interaction_event),
            "data": Serializer.serialize(self.data),
            "name": Serializer.serialize(self.name)
        }

    @classmethod
    def deserialize(cls, instance, data:dict):
        Serializer.smartDeserialize(instance, data)

    def getLocalVariables(self):
        vals = {}
        for field_name, field_data in self.field_values.items():
            vals.update({f".{field_name}": field_data["value"]})
        for data_name, data_value in self.data.items():
            vals.update({f".{data_name}": data_value})
        return vals

    def updateLocalVariables(self, locals:dict): # TODO: finish this
        for field_name, field_data in self.field_values.items():
            field_name: str
            field_data: dict
            field_value: Any = field_data["value"]
            field_type: str = field_data["type"]

    def prepFunctionMemory(self, function_memory:FunctionMemory):
        function_memory.update(self.getLocalVariables())

    def postEvaluate(self, function_memory:FunctionMemory):
        self.updateLocalVariables(function_memory.symbol_table)

    def onInteract(self, function_memory:FunctionMemory, player:Player):
        if self.interaction_event:
            self.prepFunctionMemory(function_memory)
            function_memory.addContextData({
                "#player": player
            })

            ev = function_memory.generatorEvaluateFunction(self.interaction_event)
            v = None
            try:
                v = ev.send(None)
                while isinstance(v, _EngineOperation):
                    res = yield v
                    v = ev.send(res)
            except StopIteration as e:
                v = e.value or (v if not isinstance(v, _EngineOperation) else None)
            self.postEvaluate(function_memory)
            return v

    def _load_from(self, function_memory:FunctionMemory, interaction_data:dict):
        if (i_data := interaction_data.get(self.name, None)) is not None:
            if (fields := i_data.get("fields", None)) is not None:
                for name, val in fields.items():
                    self.field_values.update({name: val})
            if (data := i_data.get("data", None)) is not None:
                for name, val in data:
                    self.data.update({name: val})

    def _get_save(self, function_memory:FunctionMemory):
        abstract_fields = self.abstract.fields

        field_save = {}

        for field_name, field_data in abstract_fields.items():
            field_name: str
            field_data: dict
            field_value = self.field_values[field_name]["value"]
            if (default := field_data.get("default", None)) is not None:
                if default != field_value:
                    field_save.update({field_name: field_value})
            else:
                field_save.update({field_name: field_value})

        data_save = {}

        for name, value in self.data.items():
            if (abstract_value := self.abstract.data.get(name, None)) is not None:
                if value != abstract_value:
                    data_save.update({name: value})
            else:
                data_save.update({name: value})

        d = {
        }
        if field_save:
            d.update({"fields": field_save})
        if data_save:
            d.update({"data": data_save})
        return d

    def _save_to(self, function_memory:FunctionMemory, save_dict:dict):
        if save := self._get_save(function_memory):
            save_dict.update({self.name: save})


