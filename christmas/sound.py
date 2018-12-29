import glob
import random

import pygame as pg

from enum import Enum


class SoundType(Enum):
    SFX_HIT = 1
    SFX_CRITICAL_HIT = 2
    SFX_BOUNCE = 3
    SFX_ATTACK = 4
    SFX_SPECIAL_ACQUIRED = 5
    SFX_SPECIAL_SHOT = 6
    SFX_COLLECT = 7

    MUSIC_IDLE = 8
    MUSIC_FIGHT = 9


class Sound:
    def __init__(self, debug_mode=False):
        self._debug_mode = debug_mode
        if self._debug_mode:
            return
        # Initialize mixer.
        pg.mixer.init()
        # Load `Sound` objects into memory.
        load_sounds = lambda d: [pg.mixer.Sound(f) for f in glob.glob(d)]
        self._sounds = {
            SoundType.MUSIC_IDLE            : load_sounds('res/sound/music/idle/*'),
            SoundType.MUSIC_FIGHT           : load_sounds('res/sound/music/fight/*'),
            SoundType.SFX_HIT               : load_sounds('res/sound/sfx/hit/*'),
            SoundType.SFX_CRITICAL_HIT      : load_sounds('res/sound/sfx/critical-hit/*'),
            SoundType.SFX_BOUNCE            : load_sounds('res/sound/sfx/bounce/*'),
            SoundType.SFX_ATTACK            : load_sounds('res/sound/sfx/attack/*'),
            SoundType.SFX_SPECIAL_ACQUIRED  : load_sounds('res/sound/sfx/special-acquired/*'),
            SoundType.SFX_SPECIAL_SHOT      : load_sounds('res/sound/sfx/special-shot/*'),
        }
        # Start game with fighting music.
        self.play(SoundType.MUSIC_FIGHT)

    def play(self, sound_type):
        if self._debug_mode:
            return
        assert(isinstance(sound_type, SoundType))
        # NOTE: There's a pg.mixer.music.queue method for song queues.
        random.choice(self._sounds[sound_type]).play()

    def pause():
        raise NotImplementedError

    def stop():
        raise NotImplementedError
