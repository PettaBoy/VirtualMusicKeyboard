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
     UI for the keyboard.

"""

import os
import tkinter as tk
from tkinter import ttk, messagebox
from tkinter.filedialog import askopenfilename, asksaveasfilename
from PIL import Image, ImageTk

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
          self.root.title("VirtualMusicKeyboard")
          self.root.geometry('%dx350'%(40+140*scales+20))
          self.piano_img = Image.open("piano.png")
          self.icon = ImageTk.PhotoImage(self.piano_img)
          self.root.iconphoto(True, self.icon)

          self.SF2 = [file for file in os.listdir("./sf2") if file.endswith('.sf2')]
          if self.SF2 == []:
               tk.messagebox.showerror(title='SF2 not found', message=
                    'Cannot find SF2 file, please check again')
               self.root.destroy()
          else:
               self.musickeyboard = MusicKeyboard(os.path.join("./sf2", self.SF2[0]))
               self.musickeyboard.set_instrument(0, 0)
          
               self.initui()

     def initui(self):
          self.keyboard_frame = tk.Frame(self.root)
          self.keyboard_frame.pack(side='bottom', fill='both', expand=True)

          self.settings_frame = tk.Frame(self.root)
          self.settings_frame.pack(side='top', fill='both', expand=True)

          self.create_keys()
          self.tuning_options()

          self.keyDown = False
          self.keyList = {}

          self.root.bind('<KeyPress>', self.keyboard_playnote)
          self.root.bind('<KeyRelease>', self.keyboard_stopnote)
          for button in self.buttons:
               self.root.bind('<Button-1>', self.mouse_playnote)
    
     def create_keys(self):
          """Creates the white and black keys of the keyboard."""
          for i in range(self.white_keys):
               self.W = tk.Button(self.keyboard_frame, bg='white')
               self.W.grid(row=0, column=i*3, rowspan=2, columnspan=3,
                    sticky='nsew')
               self.buttons.append(self.W)

          for i in range(self.white_keys-1):
               if self.black_keys[i] == 1:
                    self.B = tk.Button(self.keyboard_frame, bg='black',
                         activebackground='grey')
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

          self.display = tk.Text(self.settings_frame, width=60, height=5)
          self.display.grid(column=4, row=0, columnspan=2, rowspan=30,
               padx=5, pady=5)

          self.button_about = ttk.Button(self.settings_frame, text="About",
               width=10, command=self.about_box_open)
          self.button_about.grid(column=4, row=30, padx=5, pady=5)
          self.button_help = ttk.Button(self.settings_frame, text="Help",
               width=10, command=self.help_open)
          self.button_help.grid(column=5, row=30, padx=5, pady=5)

          beats = ["4/4", "8/8", "6/8", "2/4", "3/4", "5/4"]
          self.metronome = Metronome(self.settings_frame, beats, self.SF2)

          self.settings_frame.columnconfigure(4, weight=2)
          self.settings_frame.columnconfigure(5, weight=2)

     def mouse_playnote(self, event):
          note = self.buttons.index(event.widget)
          self.musickeyboard.play_note(note, self.channel_no.get(),
               self.__velocity.get())

     def keyboard_playnote(self, event):
         if (event.keysym in self.keyList) != True:
              self.keyList[event.keysym] = "down"
              for k in self.keyList:
                   note = db.keyboard_mappings[k]
                   self.musickeyboard.play_note(note, self.channel_no.get(),
                        self.__velocity.get())
                   self.buttons[note].config(bg='orange')
                   if note > 51:
                        self.root.after(100,
                             lambda: self.buttons[note].config(bg='black'))
                   else:
                        self.root.after(100,
                             lambda: self.buttons[note].config(bg='white'))
         self.keyDown = True

     def keyboard_stopnote(self, event):
         if (event.keysym in self.keyList) == True:
              self.keyList.pop(event.keysym)
         if len(self.keyList) == 0:
              self.keyDown = False

     def sustain_change(self):
          self.musickeyboard.sustain(self.channel_no.get(), self.__sustain.get())

     def set_instrument(self, event):
          instr_no, instr_name = self.program_name.get().split('  ')
          self.musickeyboard.set_instrument(self.channel_no.get(), int(instr_no))

     def about_box_open(self):
          about_box = tk.Toplevel(self.root)
          about_box.title("About")
          label_icon = ttk.Label(about_box, image=self.icon, width=5)
          label_icon.grid(column=0, row=0, padx=5, pady=5)
          label_title = ttk.Label(about_box, text="VirtualMusicKeyboard",
               font=("Arial", 20))
          label_title.grid(column=1, row=0, padx=5, pady=5)
          description = "A music keyboard experience, on your computer."
          label_description = ttk.Label(about_box, text=description,
               font=("Arial", 10))
          label_description.grid(column=0, row=1, columnspan=2, padx=5, pady=5)
          license_cum_copyright = ("This application is licensed under the GNU"
               " General Public License." "\n" "See the license file for more" 
               " information." "\n"
               "Copyright (C) 2021, Sishir Sivakumar."
               )
          label_copyrightcumlicense = ttk.Label(about_box,
               text=license_cum_copyright, font=("Arial", 10))
          label_copyrightcumlicense.grid(column=0, row=2, columnspan=2, padx=5,
               pady=5)
          
     def help_open(self):
          os.system("start README.txt")
