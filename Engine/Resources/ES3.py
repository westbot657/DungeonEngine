# pylint: disable=W,R,C,import-error

class EngineScript:
    _scripts = {}


    def __new__(cls, script_file, do_analysis=False):
        script_name = f"{script_file.replace("\\", "/").replace(".ds", "").replace(".dungeon_script", "")}.ds"
        
        if script_name in cls._scripts:
            return cls._scripts[script_name]

        else:
            script = super().__new__(cls)
            cls._scripts.update({script_name: script})
            script.init(script_name, do_analysis)
            return script
        
        ...
    
    def init(self, script_name, do_analysis=False):
        self.script_name = script_name
        
    
