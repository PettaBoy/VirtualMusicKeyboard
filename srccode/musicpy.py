# -*- coding: utf-8 -*-
"""

    Note sounds and tunings for the keyboard.
    
"""

from os import sys
from mingus.containers import *
from mingus.midi import fluidsynth
import database as db

class MusicKeyboard:
    def __init__(self, SF2=None):
        if not fluidsynth.init(SF2):
            raise FileNotFoundError('The specified file cannot be found.')
            sys.exit(1)

    def play_note(self, key_id, channel=0, velocity=127):
        """Determines the number assigned to a white key and sends a request to play
        the corresponding note to the fluidsynth server."""
        if key_id < 52:
            n = Note(db.white_note_names[(key_id+5)%7])
            n.octave, n.velocity = (key_id+5)//7, velocity
            fluidsynth.play_Note(n, channel)
        else:
            n = Note(db.black_note_names[(key_id-48)%5])
            n.octave, n.velocity = (key_id-48)//5, velocity
            fluidsynth.play_Note(n, channel)

    def set_instrument(self, channel, instrument_no):
        fluidsynth.set_instrument(channel, instrument_no)

    def set_volume(self, channel, volume):
        fluidsynth.control_change(channel, 7, volume)

    def pan(self, channel, pan):
        fluidsynth.control_change(channel, 10, pan)

    def modulation(self, channel, modulation):
        fluidsynth.control_change(channel, 11, modulation)

    def sustain(self, channel, sustain):
        fluidsynth.control_change(channel, 64, sustain)
