# -*- coding: utf-8 -*-
"""

UI for the keyboard.

"""

import tkinter as tk
from tkinter import ttk
import musicpy, database as db
from metronome import Metronome

class Keyboard(tk.Frame):
     """Set up the UI for the keyboard."""
    
     def __init__(self, mainwindow, white_keys=None, black_keys=None):
          tk.Frame.__init__(self, mainwindow, white_keys=None, black_keys=None)
          self.mainwindow = mainwindow

          self.keyboard_frame = tk.Frame(self.mainwindow)
          self.keyboard_frame.pack(side='bottom', fill='both', expand=True)

          self.settings_frame = tk.Frame(self.mainwindow)
          self.settings_frame.pack(side='top', fill='both', expand=True)

          self.buttons_white = []
          self.buttons_black = []

          self.create_keys(white_keys, black_keys)

          self.tuning_options()

          self.mainwindow.bind('<Key>',
               lambda event: self.keyboard_playnote(event,
                    self.program_name.get(), int(self.sustain.get()),
                    int(self.channel_no.get()), int(self.velocity.get())))
    
     def create_keys(self, white_keys, black_keys):
          """Creates the white and black keys of the keyboard."""
          for i in range(white_keys):
               self.W = tk.Button(self.keyboard_frame, bg='white')
               self.W["command"] = lambda i=i: musicpy.play_white_note(i,
                    self.program_name.get(), int(self.sustain.get()),
                    int(self.channel_no.get()), int(self.velocity.get()))
               self.W.grid(row=0, column=i*3, rowspan=2, columnspan=3,
                    sticky='nsew')
               self.buttons_white.append(self.W)

          for i in range(white_keys - 1):
               if black_keys[i] == 1:
                    self.B = tk.Button(self.keyboard_frame, bg='black',
                        activebackground='grey')
                    self.B["command"] = lambda i=i: musicpy.play_black_note(i,
                        self.program_name.get(), int(self.sustain.get()),
                        int(self.channel_no.get()), int(self.velocity.get()))
                    self.B.grid(row=0, column=(i*3)+2, rowspan=1, columnspan=2,
                         sticky='nsew')
                    self.buttons_black.append(self.B)
               if black_keys[i] == 0:
                    self.buttons_black.insert(i, 0)

          for i in range(white_keys * 3):
               self.keyboard_frame.columnconfigure(i, weight=1)

          for i in range(2):
               self.keyboard_frame.rowconfigure(i, weight=1)

     def tuning_options(self):
          """Settings required for a wholesome music keyboard experience."""
          font_used = ("Arial", 10)

          self.label_channel = ttk.Label(self.settings_frame, text='Channel:',
               font=font_used).grid(column=0, row=5)
          self.channel_no = tk.IntVar()
          self.channel = ttk.Combobox(self.settings_frame, width=3,
               state='readonly', textvariable=self.channel_no)
          self.channel['values'] = ([i for i in range(16)])
          self.channel.grid(column=1, row=5)
          self.channel.current(0)
        
          self.label_velocity = ttk.Label(self.settings_frame, text='Velocity:',
               font=font_used).grid(column=2, row=5)
          self.velocity = ttk.Spinbox(self.settings_frame, width=5, from_=0,
               to=127, state='readonly')
          self.velocity.grid(column=3, row=5, sticky='w')
          self.velocity.set(127)

          self.separator1 = ttk.Separator(self.settings_frame)
          self.separator1.grid(column=0, row=10)
        
          self.label_sustain = ttk.Label(self.settings_frame, text='Sustain:',
               font=font_used).grid(column=0, row=15)
          self.sustain = ttk.Spinbox(self.settings_frame, width=3, from_=0,
               to=127, state='readonly')
          self.sustain.grid(column=1, row=15)
          if int(self.channel_no.get()) == 9:
               self.sustain.set(0)
          else:
               self.sustain.set(0)
        
          self.label_program = ttk.Label(self.settings_frame, text='Program:',
               font=font_used).grid(column=2, row=15)
          self.program_name = tk.StringVar()
          self.program = ttk.Combobox(self.settings_frame, width=15,
               state='readonly', textvariable=self.program_name)
          self.program['values'] = ([str(i)+'  '+str(j) for i,
               j in db.program_values.items()])
          if int(self.channel_no.get()) == 9:
               self.program.current(0)
          else:
               self.program.current(0)
          self.program.grid(column=3, row=15)
        
          beats = ["4/4", "6/8", "2/4", "3/4"]
          self.metronome = Metronome(self.settings_frame, beats)

     def keyboard_playnote(self, event, prog, sustain=0, channel=0, velocity=127):
          note = db.keyboard_mappings[event.keysym]
          if note < 42:
               musicpy.play_white_note(note, prog, sustain, channel, velocity)
               self.buttons_white[note].config(bg='orange')
               self.mainwindow.after(100,
                    lambda: self.buttons_white[note].config(bg='white'))
          elif note > 42:
               musicpy.play_black_note(note-28, prog, sustain, channel, velocity)
               self.buttons_black[note-28].config(bg='orange')
               self.mainwindow.after(100,
                    lambda: self.buttons_black[note-28].config(bg='black'))
