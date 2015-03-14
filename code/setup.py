import sys
from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need fine tuning.
build_exe_options = {
    "packages": ["os"], 
    "excludes": ["tkinter"], 
    "include_files": ["..\\assets"],
    "create_shared_zip": True,
    "include_in_shared_zip": True,
    "include_msvcr": True
}

# GUI applications require a different base on Windows (the default is for a
# console application).
base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(  name = "guifoo",
        version = "0.1",
        description = "The Chase",
        options = {"build_exe": build_exe_options},
        executables = [Executable("Chase.py", base=base)])
