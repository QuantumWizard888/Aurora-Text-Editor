@echo off
REM ### Nuitka Python to C convert and compile ###
REM ### Standard build ###
python -m nuitka --disable-console --lto=yes aurora_text_editor.py