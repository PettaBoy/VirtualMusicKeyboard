import tkinter as tk
from gui import Keyboard
from musicpy import initsf2

initsf2("./GeneralUser GS 1.471/GeneralUser GS v1.471.sf2")

scales = 7
white_keys = 2 + 7 * scales + 1
black_keys = [1, 0] + [1, 1, 0, 1, 1, 1, 0] * scales

keyboard = tk.Tk()
keyboard.title("Virtual Music Keyboard")
keyboard.geometry('%dx250'%(40+140*scales+20))
icon = tk.PhotoImage(file="./piano.png")
keyboard.iconphoto(True, icon)
Keyboard(keyboard, white_keys, black_keys).pack()
keyboard.mainloop()
