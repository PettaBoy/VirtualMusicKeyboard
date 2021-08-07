import sys
from cx_Freeze import setup, Executable

build_exe_options = {"packages": ["VirtualMusicKeyboard"],
                     "include_files": ["VirtualMusicKeyboard/sf2",
                                  "VirtualMusicKeyboard/piano.png"]}

base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(
    name = "VirtualMusicKeyboard",
    version = "0.1",
    description = "A music keyboard experience, on your computer.",
    options = {"build_exe": build_exe_options},
    executables = [Executable("./VirtualMusicKeyboard/__init__.py", base=base)]
)
