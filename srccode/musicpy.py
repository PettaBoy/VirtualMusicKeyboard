# -*- coding: utf-8 -*-

# VirtualMusicKeyboard - A music keyboard experience, on your computer.
# Copyright (C) 2021, Sishir Sivakumar

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

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
