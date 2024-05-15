@echo off
REM ### Nuitka Python to C convert and compile ###
REM ### Standalone build ###
python -m nuitka --disable-console --lto=yes --enable-plugin=tk-inter --onefile aurora_text_editor.py