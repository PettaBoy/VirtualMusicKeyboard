# -*- coding: utf-8 -*-
"""
    Metronome Section of the Keyboard.

"""

import tkinter as tk
from tkinter import ttk
from winsound import Beep
from mingus.midi import fluidsynth

class Metronome:
    """Create Metronome app with class instance."""

    def __init__(self, frame, beats):
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
        label_metronome.grid(column=7, row=10, rowspan=10)
        
        spinbox_bpm = ttk.Spinbox(self.frame, width=5, from_=60, to=300,
                                  state='readonly')
        spinbox_bpm.grid(row=0, column=9)
        spinbox_bpm.set(60)

        spinbox_beats = ttk.Spinbox(self.frame, width=5, values=self.beats,
                                wrap=True, state='readonly')
        spinbox_beats.grid(row=0, column=10)
        spinbox_beats.set(self.beats[0])

        label_bpm = ttk.Label(self.frame, text="BPM:")
        label_bpm.grid(row=0, column=8)

        label_time = ttk.Label(self.frame, text="Time:")
        label_time.grid(row=10, column=8)

        label_count = ttk.Label(self.frame, textvariable=self.var,
                                font=("Arial", 10))
        label_count.grid(row=10, column=9, columnspan=2)

        button_start = ttk.Button(self.frame, text="Start", width=10,
                              command=lambda: self.start_counter(spinbox_bpm,
                                                                 spinbox_beats))
        button_start.grid(row=20, column=9)

        button_stop = ttk.Button(self.frame, text="Stop", width=10,
                             command=lambda: self.stop_counter())
        button_stop.grid(row=20, column=10)

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

            if self.beat == 6:  # 6/8 time
                self.time = int((60 / (self.bpm / .5) - 0.1) * 1000)
            else:
                self.time = int((60 / self.bpm - 0.1) * 1000)  # Math for delay

            self.count += 1
            self.var.set(self.count)

            if self.count == 1:
                Beep(880, 100)
            elif self.count >= self.beat:
                self.count = 0
                Beep(440, 100)
            else:
                Beep(440, 100)

            # Calls this method after a certain amount of time.
            self.frame.after(self.time, lambda: self.counter(spinbox))
