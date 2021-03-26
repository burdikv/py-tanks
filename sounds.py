import pygame


class Sounds(object):
    def __init__(self):
        self.sounds = {}
        sound_files = {"sound.shoot": "Sounds\\mixkit-war-explosions-2773.wav",
                       "sound.hit": "Sounds\\mixkit-hitting-metal-armor-2775.wav",
                       "sound.explosion": "Sounds\\mixkit-war-field-explosion-1702.wav",
                       "sound.tank": "Sounds\\mixkit-tank-engine-working-2753.wav",
                       "sound.hit.shield": "Sounds\\mixkit-spring-metal-hit-2302.wav"}
        for name in sound_files:
            self.sounds[name] = [sound_files[name], pygame.mixer.Sound(sound_files[name])]

    def play(self, name):
        if name in self.sounds:
            pygame.mixer.find_channel(True).play(self.sounds[name][1])
            # self.sounds[name][1].play()

    def stop(self, name):
        if name in self.sounds:
            self.sounds[name][1].stop()

    def get_sound(self, name):
        if name in self.sounds:
            return self.sounds[name][1]

    def clone_sound(self, name):
        if name in self.sounds:
            return pygame.mixer.Sound(self.sounds[name][0])
        else:
            return None


"""
    def is_playing(self, name):
        if name in self.sounds:
            return self.sounds[name][1].isPlaying()
        else:
            return False
"""
