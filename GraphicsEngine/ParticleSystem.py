# pylint: disable=W,R,C,import-error

from UIElement import UIElement

import glob

DEFAULT_PARTICLE_CONFIGS = {
    "animated_transition": {
        "loop": False,
        "duration": 1,
        "fade-in": {
            "duration": 0
        },
        "fade-out": {
            "duration": 0
        },
        "particle": {
            "sheet-source": "", # Path to sprite sheet
            "sheet-segments": [1, 1] # how many frames across width, height
        }
    }
}

class ParticleSystem(UIElement):
    
    class ParticleEffect:
        
        class ParticleInstance:
            def __init__(self, x, y, parent):
                self.x = x
                self.y = y
                self.parent = parent
            
            def _event(self, editor, X, Y):
                ...
                
            def _update(self, editor, X, Y):
                ...
        
        def __init__(self, configuration:dict):
            self.configuration = configuration
            
        def instance(self, position: tuple[int, int]) -> ParticleInstance:
            return ParticleSystem.ParticleEffect.ParticleInstance(*position, self)
    
    def __init__(self):
        self.active_particles = {"normal": []}

    def clear_particles(self, effect_types:list=None):
        if effect_types is None:
            self.active_particles.clear()
            self.active_particles.update({"normal": []})
        else:
            for t in effect_types:
                if t in self.active_particles:
                    self.active_particles.pop(t)

    def spawn(self, particle_effect: ParticleEffect, position: tuple[int, int], effect_type="normal"):
        if effect_type not in self.active_particles:
            self.active_particles.update({effect_type: []})
        self.active_particles[effect_type].insert(0, particle_effect.instance(position))


    def _event(self, editor, X, Y):
        for effect_type, particles in self.active_particles.items():
            for effect in particles:
                effect._event(editor, X, Y)
        
    def _update(self, editor, X, Y):
        for effect_type, particles in self.active_particles.items():
            for effect in particles:
                effect._update(editor, X, Y)
