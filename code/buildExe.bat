@echo off
rem This script builds the exes for The Chase
rmdir /s /q build
python setup.py build
rmdir /S /Q ..\lastbuild
xcopy /S "build\exe.win32-3.4\*" "..\lastbuild\"