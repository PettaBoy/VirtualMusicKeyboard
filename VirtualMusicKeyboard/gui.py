# -*- coding: utf-8 -*-
"""

UI for the keyboard.

"""

import os
import tkinter as tk
from tkinter import ttk, messagebox
from tkinter.filedialog import askopenfilename, asksaveasfilename

from musicpy import MusicKeyboard
import database as db
from metronome import Metronome

class App:
     """Set up the UI for the keyboard."""

     buttons = []
    
     def __init__(self, root, scales=7):
          self.root = root
          self.white_keys = 2 + 7*scales + 1
          self.black_keys = [1, 0] + [1, 1, 0, 1, 1, 1, 0]*scales
          self.root.title("Virtual Piano Keyboard")
          self.root.geometry('%dx300'%(40+140*scales+20))
          icon = tk.PhotoImage(file="./piano.png")
          self.root.iconphoto(True, icon)

          SF2 = [file for file in os.listdir("./sf2") if file.endswith('.sf2')]
          if SF2 == []:
               tk.messagebox.showerror(title='SF2 not found', message=
                    'Cannot find SF2 file, please check again')
               self.root.destroy()
          else:
               print(SF2[0])
               self.musickeyboard = MusicKeyboard(os.path.join("./sf2", SF2[0]))
               self.musickeyboard.set_instrument(0, 0)
          
               self.initui()

     def initui(self):
          self.keyboard_frame = tk.Frame(self.root)
          self.keyboard_frame.pack(side='bottom', fill='both', expand=True)

          self.settings_frame = tk.Frame(self.root)
          self.settings_frame.pack(side='top', fill='both', expand=True)

          self.create_keys()
          self.tuning_options()

          self.root.bind('<Key>', self.keyboard_playnote)
          for button in self.buttons:
               self.root.bind('<Button-1>', self.mouse_playnote)
    
     def create_keys(self):
          """Creates the white and black keys of the keyboard."""
          for i in range(self.white_keys):
               self.W = tk.Button(self.keyboard_frame, bg='white',
                    command=lambda i=i: print(i))
               self.W.grid(row=0, column=i*3, rowspan=2, columnspan=3,
                    sticky='nsew')
               self.buttons.append(self.W)

          for i in range(self.white_keys-1):
               if self.black_keys[i] == 1:
                    self.B = tk.Button(self.keyboard_frame, bg='black',
                         activebackground='grey', command=lambda i=i: print(i))
                    self.B.grid(row=0, column=(i*3)+2, rowspan=1, columnspan=2,
                         sticky='nsew')
                    self.buttons.append(self.B)

          for i in range(self.white_keys*3):
               self.keyboard_frame.columnconfigure(i, weight=1)

          for i in range(2):
               self.keyboard_frame.rowconfigure(i, weight=1)

     def tuning_options(self):
          """Settings required for a wholesome music keyboard experience."""
          font_used = ("Arial", 10)

          self.label_channel = ttk.Label(self.settings_frame, text='Channel:',
               font=font_used).grid(column=0, row=0, padx=5, pady=5)
          self.channel_no = tk.IntVar()
          self.channel = ttk.Combobox(self.settings_frame, width=3,
               state='readonly', textvariable=self.channel_no)
          self.channel['values'] = ([i for i in range(16)])
          self.channel.grid(column=1, row=0, padx=5, pady=5)
          self.channel.current(0)
        
          self.label_velocity = ttk.Label(self.settings_frame, text='Velocity:',
               font=font_used).grid(column=2, row=0, padx=5, pady=5)
          self.__velocity = tk.IntVar()
          self.velocity = ttk.Spinbox(self.settings_frame, width=5, from_=0,
               to=127, textvariable=self.__velocity, state='readonly')
          self.velocity.grid(column=3, row=0, sticky='w', padx=5, pady=5)
          self.velocity.set(127)
        
          self.label_sustain = ttk.Label(self.settings_frame, text='Sustain:',
               font=font_used).grid(column=0, row=10, padx=5, pady=5)
          self.__sustain = tk.IntVar()
          self.sustain = ttk.Spinbox(self.settings_frame, width=3, from_=0,
               to=127, textvariable=self.__sustain, state='readonly',
               command=self.sustain_change)
          if int(self.channel_no.get()) == 9:
               self.sustain.set(0)
          else:
               self.sustain.set(0)
          self.sustain.grid(column=1, row=10, padx=5, pady=5)
        
          self.label_program = ttk.Label(self.settings_frame, text='Program:',
               font=font_used).grid(column=2, row=10, padx=5, pady=5)
          self.program_name = tk.StringVar()
          self.program = ttk.Combobox(self.settings_frame, width=15,
               state='readonly', textvariable=self.program_name)
          self.program['values'] = ([str(i)+'  '+str(j) for i,
               j in db.program_values.items()])
          if int(self.channel_no.get()) == 9:
               self.program.current(0)
          else:
               self.program.current(0)
          self.program.grid(column=3, row=10, padx=5, pady=5)
          self.program.bind('<<ComboboxSelected>>', self.set_instrument)

     def keyboard_playnote(self, event):
          note = db.keyboard_mappings[event.keysym]
          self.musickeyboard.play_note(note, self.channel_no.get(),
               self.__velocity.get())
          self.buttons[note].config(bg='orange')
          if note > 51:
               self.root.after(100,
                    lambda: self.buttons[note].config(bg='black'))
          else:
               self.root.after(100,
                    lambda: self.buttons[note].config(bg='white'))

     def mouse_playnote(self, event):
          note = self.buttons.index(event.widget)
          self.musickeyboard.play_note(note, self.channel_no.get(),
               self.__velocity.get())

     def sustain_change(self):
          self.musickeyboard.sustain(self.channel_no.get(), self.__sustain.get())

     def set_instrument(self, event):
          instr_no, instr_name = self.program_name.get().split('  ')
          self.musickeyboard.set_instrument(self.channel_no.get(), int(instr_no))
