# pylint: disable=W,R,C,import-error


import pygame

class SoundSystem:
    _sound_system = None
    
    @classmethod
    def initialize(cls):
        pygame.mixer.init()
    
    class Audio:
        def __init__(self, name, category, system, sound:pygame.mixer.Sound):
            self.name = name
            self.category = category
            self._system = system
            self.sound = sound
            self.volume = 1
            
        def play(self, loops=0, maxtime=0, fade_ms=0):
            self.sound.play(loops, maxtime, fade_ms)
        
        def stop(self):
            self.sound.stop()
        
        def set_volume(self, volume):
            self.volume = volume
            self.sound.set_volume(volume * self._system.volumes[self.category])
    
    def __new__(cls, *args, **kwargs):
        if not cls._sound_system:
            cls._sound_system = super().__new__(cls)
            cls._sound_system.init(*args, **kwargs)
        return cls._sound_system
    
    def get_audio(self, name:str, category:str):
        for audio in self.sounds[category]:
            if audio.name == name:
                return audio
        return None
    
    def init(self):
        self.sounds = {
            "game": [],
            "ui": []
        }
        self.volumes = {
            "game": 1,
            "ui": 0.25
        }
        
    def load(self, file, name:str, category:str) -> Audio:
        audio = pygame.mixer.Sound(file)
        if category not in self.sounds:
            self.sounds.update({category: []})
            self.volumes.update({category: 1})
        
        obj = SoundSystem.Audio(name, category, self, audio)
        
        self.sounds[category].append(obj)
        return obj
        
    def set_volume(self, category:str, volume:float):
        self.volumes.update({category: volume})
        
        for audio in self.sounds[category]:
            audio.set_volume(audio.volume)
        
        
    


