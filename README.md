# Aurora Text Editor
<img src = "https://github.com/QuantumWizard888/Aurora-Text-Editor/blob/main/PREVIEW.PNG">

## === About ===
Minimalistic text editor created with Python and Tkinter. If you need to write simple TXT files so this is what you need. No more, no less.

## === Features ===
- Themes
- Font Styles
- Basic text statistics
- Portable

## === How to compile ===
To compile use [Nuitka](https://nuitka.net/) (Python code to C code converter, which then uses the default C compiler in your OS to build the program):
```
python -m nuitka aurora_text_editor.py
```
And then use [UPX](https://upx.github.io/) to decrease file size:
```
upx aurora_text_editor.exe
```

For standalone EXE and portability add change the **Nuitka Python to C compiler options** section in the source code file to this:
```
# <--- Nuitka Python to C compiler options
# nuitka-project: --disable-console
# nuitka-project: --lto=yes
# nuitka-project: --enable-plugin=tk-inter
# nuitka-project: --onefile
# --->
```

## === Why? ===
Consider this program as a lesson for those who want to write their own text editor or other GUI program using Python and Tkinter. Enjoy!
