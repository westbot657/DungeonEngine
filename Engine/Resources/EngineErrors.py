# pylint: disable=[W,R,C,import-error]

class EngineError(Exception):
    def __repr__(self):
        return "\n".join(self.args)

class EngineBreak(Exception): pass

class InvalidObjectError(EngineError):
    def __init__(self, *args):
        super().__init__("InvalidObjectError:", *args)

class FunctionCallError(EngineError): # Error when function can't be called
    def __init__(self, *args):
        super().__init__("FunctionCallError:", *args)

class FunctionLoadError(EngineError): # Error when function can't load/can't be found
    def __init__(self, *args):
        super().__init__("FunctionLoadError:", *args)

class FunctionRunError(EngineError): # Error with code within a function
    def __init__(self, *args):
        super().__init__("FunctionRunError:", *args)

class MemoryError(EngineError): # Error with FunctionMemory
    def __init__(self, *args):
        super().__init__("MemoryLoadError:", *args)

class IdentifierError(EngineError):
    def __init__(self, *args):
        super().__init__("IdentifierError:", *args)

class LocationError(EngineError):
    def __init__(self, *args):
        super().__init__("LocationError:", *args)

class ParseError(EngineError):
    def __init__(self, *args):
        super().__init__("ParseError:", *args)

class CombatError(EngineError):
    def __init__(self, *args):
        super().__init__("CombatError:", *args)

class FunctionError(EngineError):
    def __init__(self, *args):
        super().__init__("FunctionError:", *args)

class UnknownPlayerError(EngineError):
    def __init__(self, player_id:int):
        super().__init__(f"UnknownPlayerError: No player exists with id: '{player_id}'")

class CurrencyError(EngineError):
    def __init__(self, *args):
        super().__init__("CurrencyError:", *args)

class ScriptError(EngineError):
    def __init__(self, *args):
        super().__init__(f"ScriptError:", *args)
    def __repr__(self):
        return "\n".join(self.args)

class FinalScriptError(EngineError):
    def __init__(self, *args):
        super().__init__(*args)
    def __repr__(self):
        return "\n".join(self.args)
class LexerError(ScriptError):
    def __init__(self, *args):
        self.args = args

class ParserError(ScriptError):
    def __init__(self, *args):
        self.args = args

class EOF(ScriptError):
    def __init__(self, *args):
        super().__init__(f"EOF:", *args)