import sys
from cx_Freeze import setup, Executable

build_exe_options = {"packages": ["srccode"]}

base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(
    name = "VirtualMusicKeyboard",
    version = "0.1",
    description = "A music keyboard experience, on your computer.",
    options = {"build_exe": build_exe_options},
    executables = [Executable("./srccode/__init__.py",
                              icon="piano.ico",
                              target_name="VirtualMusicKeyboard.exe", base=base)]
)
