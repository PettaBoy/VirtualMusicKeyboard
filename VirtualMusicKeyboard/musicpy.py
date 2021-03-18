# -*- coding: utf-8 -*-
"""

    Note sounds and tunings for the keyboard.
    
"""

from os import sys
import time
from mingus.containers import *
from mingus.midi import fluidsynth, midi_file_out as mfo
import database as db

def initsf2(SF2):
    try:
        fluidsynth.init(SF2)
    except:
        raise FileNotFoundError('The specified file cannot be found.')
        sys.exit(1)

def play_white_note(note, prog, sustain=0, channel=0, velocity=127):
    """Determines the number assigned to a white key and sends a request to play
    the corresponding note to the fluidsynth server."""
    if channel == 9:
        n = Note(db.white_note_names[(note+5)%7])
        n.octave, n.velocity = (note+5)//7, velocity
        fluidsynth.play_Note(n, channel)
    else:
        instr_no, instr_name = prog.split('  ')
        fluidsynth.set_instrument(channel, int(instr_no))
        fluidsynth.control_change(channel, 64, sustain)
        n = Note(db.white_note_names[(note+5)%7])
        n.octave, n.channel, n.velocity = (note+5)//7, channel, velocity
        fluidsynth.play_Note(n)
    
def play_black_note(note, prog, sustain=0, channel=0, velocity=127):
    """Same as play_white_note, but on a black key."""
    if channel == 9:
        n = Note(db.black_note_names[(note+5)%7])
        n.octave, n.velocity = (note+5)//7, velocity
        fluidsynth.play_Note(n, channel)
    else:
        instr_no, instr_name = prog.split('  ')
        fluidsynth.set_instrument(channel, int(instr_no))
        fluidsynth.control_change(channel, 64, sustain)
        n = Note(db.black_note_names[(note+5)%7])
        n.octave, n.channel, n.velocity = (note+5)//7, channel, velocity
        fluidsynth.play_Note(n)
