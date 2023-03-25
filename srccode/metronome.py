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
    Metronome Section of the Keyboard.
    Taken from https://github.com/Kwisses/Metronome

"""

import tkinter as tk
from tkinter import ttk
from winsound import Beep
from mingus.midi import fluidsynth

class Metronome:
    """Create Metronome app with class instance."""

    def __init__(self, frame, beats, SF2=None):
        if not fluidsynth.init(SF2):
            raise FileNotFoundError('The specified file cannot be found.')
        self.frame = frame
        self.beats = beats

        self.start = False
        self.bpm = 0
        self.count = 0
        self.beat = 0
        self.time = 0

        self.var = tk.StringVar()
        self.var.set(self.count)

        self.interface()

    def interface(self):
        """Set interface for Metronome app."""
        label_metronome = ttk.Label(self.frame, text="Metronome")
        label_metronome.grid(column=6, row=0, rowspan=30, padx=5, pady=5)

        label_type = ttk.Label(self.frame, text="Type:")
        label_type.grid(column=7, row=0, padx=5, pady=5)
        self.__type = tk.StringVar()
        self.combobox_type = ttk.Combobox(self.frame, width=10, state='readonly',
            textvariable=self.__type)
        self.combobox_type['values'] = ("Beep", "Percussion-1", "Percussion-2")
        self.combobox_type.current(0)
        self.combobox_type.grid(column=8, row=0, columnspan=2, padx=5, pady=5)
        self.combobox_type.bind('<<ComboboxSelected>>', self.set_defset)
        
        self.spinbox_bpm = ttk.Spinbox(self.frame, width=5, from_=60, to=300,
            state='readonly')
        self.spinbox_bpm.grid(row=10, column=8, padx=5, pady=5)
        self.spinbox_bpm.set(60)

        self.spinbox_beats = ttk.Spinbox(self.frame, width=5, values=self.beats,
            wrap=True, state='readonly')
        self.spinbox_beats.grid(row=10, column=9, padx=5, pady=5)
        self.spinbox_beats.set(self.beats[0])

        label_bpm = ttk.Label(self.frame, text="BPM:")
        label_bpm.grid(row=10, column=7, padx=5, pady=5)

        label_time = ttk.Label(self.frame, text="Beat number:")
        label_time.grid(row=20, column=7, padx=5, pady=5)

        label_count = ttk.Label(self.frame, textvariable=self.var,
            font=("Arial", 10))
        label_count.grid(row=20, column=8, columnspan=2, padx=5, pady=5)

        button_start = ttk.Button(self.frame, text="Start", width=10,
            command=lambda: self.start_counter(self.spinbox_bpm,
                self.spinbox_beats))
        button_start.grid(row=30, column=8, padx=5, pady=5)

        button_stop = ttk.Button(self.frame, text="Stop", width=10,
            command=lambda: self.stop_counter())
        button_stop.grid(row=30, column=9, padx=5, pady=5)

    def start_counter(self, spinbox1, spinbox2):
        """Start counter if self.start is False(prevents multiple starts)."""
        if not self.start:
            self.start = True
            self.bpm = int(spinbox1.get())
            self.counter(spinbox2)

    def stop_counter(self):
        """Stop counter by setting self.start to False."""
        self.start = False

    def counter(self, spinbox):
        """Control counter display and audio with calculated time delay."""
        if self.start:
            self.beat = int(spinbox.get()[0])
            self.note_storage = int(spinbox.get()[2])

            if self.note_storage == 8:  # 6/8 or 8/8 time
                self.time = int((60 / (self.bpm / .5)) * 1000)
            else:
                self.time = int((60 / self.bpm) * 1000)  # Math for delay

            self.count += 1
            self.var.set(self.count)

            type_ = self.__type.get()
            if type_ == "Beep":
                self.winbeep()
            elif type_ == "Percussion-1":
                self.percussion_1()
            elif type_ == "Percussion-2":
                self.percussion_2()

            # Calls this method after a certain amount of time.
            self.frame.after(self.time, lambda: self.counter(spinbox))

    def set_defset(self, event):
        type_ = self.__type.get()
        if type_ == "Beep":
            self.spinbox_bpm.set(60)
            self.spinbox_beats.set(self.beats[0])
            self.count = 0
            self.var.set(self.count)
        elif type_ == "Percussion-1":
            self.spinbox_bpm.set(120)
            self.spinbox_beats.set(self.beats[1])
            self.count = 0
            self.var.set(self.count)
        elif type_ == "Percussion-2":
            self.spinbox_bpm.set(90)
            self.spinbox_beats.set(self.beats[2])
            self.count = 0
            self.var.set(self.count)

    def winbeep(self):
        if self.count == 1:
            Beep(880, 100)
        elif self.count >= self.beat:
            self.count = 0
            Beep(440, 100)
        else:
            Beep(440, 100)

    def percussion_1(self):
        if self.count % 4 == 1:
            fluidsynth.play_Note(24, 9, 127)
            fluidsynth.play_Note(30, 9, 127)
        elif self.count % 4 == 3:
            fluidsynth.play_Note(26, 9, 127)
            fluidsynth.play_Note(30, 9, 127)
        elif self.count >= self.beat:
            self.count = 0
            fluidsynth.play_Note(30, 9, 127)
        else:
            fluidsynth.play_Note(30, 9, 127)

    def percussion_2(self):
        if self.count % 6 == 1:
            fluidsynth.play_Note(24, 9, 127)
            fluidsynth.play_Note(30, 9, 127)
        elif self.count % 6 == 4:
            fluidsynth.play_Note(26, 9, 127)
            fluidsynth.play_Note(30, 9, 127)
        elif self.count >= self.beat:
            self.count = 0
            fluidsynth.play_Note(30, 9, 127)
        else:
            fluidsynth.play_Note(30, 9, 127)
