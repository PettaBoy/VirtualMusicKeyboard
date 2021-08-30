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
    Use to build an executable using cx_Freeze.

"""

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
