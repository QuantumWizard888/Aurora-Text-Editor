
#* Aurora Text Editor
#? Minimalistic text editor
#? Version: 0.7.1

from tkinter import *
from tkinter.messagebox import askyesno, QUESTION, showwarning
from tkinter import filedialog as fd
import os

# <--- Nuitka Python to C compiler options
# nuitka-project: --disable-console
# nuitka-project: --lto=yes
# --->

# <--- Global variables
is_saved = False
file_name = ''
is_modified = False
theme_name = 'Light'
font_size = 11
font_name = 'Courier'
font_style = 'normal'

def is_modified_text_event(Event):
    
    global is_modified
    global is_saved

    is_modified = True
    is_saved = False

# --->


# <--- Window init
prog_name = 'Aurora Text Editor'
prog_version = ' v0.7.1'
window = Tk()
window.title(prog_name+prog_version)
# --->

# <--- Widgets init
text = Text(master=window, wrap=WORD, font=(font_name, font_size, font_style))
scroll = Scrollbar(master=window)
status_bar = Label(master=window, relief=SUNKEN, anchor=SW)
# --->


# <--- Widgets config
text.config(yscrollcommand=scroll.set)
scroll.config(command=text.yview)
# --->


# <--- GUI layout
status_bar.pack(side=BOTTOM, fill=X)
text.pack(side=LEFT, fill=BOTH, expand=True)
text.focus() # Focusing on Text widget
scroll.pack(side=RIGHT, fill=Y)
# --->


# <--- status_bar_info func
def status_bar_info():
    
    all_text = text.get('1.0', END)
    newlines_count = all_text.count('\n')
    symbols_count = len(all_text) - newlines_count
    words_count = len((all_text).split())
    
    status_bar.config(text='Lines: ' + str(newlines_count) + '    Length: ' + str(symbols_count) + '    Words: ' + str(words_count) + '    Length (Bytes): ' + str(text_len_in_bytes_utf8()) + '    Is Saved: ' + str(is_saved) + '    Is Modified: ' + str(is_modified) + '\t\tTheme: ' + theme_name + '    Font: ' + font_name + '    Font size: ' + str(font_size) + '    Font style: ' + font_style)

    window.after(500, status_bar_info)

def text_len_in_bytes_utf8() -> int:
    
    return len(text.get(1.0, 'end-1c').encode('utf-8'))
    
# --->


# <--- on_start() and on_exit() functions

def set_window_default_geometry():
    
    global theme_name
    theme_name = 'Light'

    window_w = 1200
    window_h = 800
    screen_w = window.winfo_screenwidth()
    screen_h = window.winfo_screenheight()
    x = (screen_w/2) - (window_w/2)
    y = (screen_h/2) - (window_h/2)
    window.geometry('%dx%d+%d+%d' % (window_w, window_h, x, y))

    text.configure(font=('Courier', 11, 'normal'))
    on_menu_set_theme('Light')


def save_window_geometry():

    global theme_name
    global font_name
    global font_size
    global font_style

    with open("aurora_editor.conf", "w") as conf_file:
        conf_file_list = [window.geometry()+'\n', theme_name+'+'+font_name+'+'+str(font_size)+'+'+font_style]
        conf_file.writelines(conf_file_list)


def on_start():
    
    global theme_name
    global font_name
    global font_size
    global font_style

    if os.path.isfile("aurora_editor.conf"):

        try: 
            with open("aurora_editor.conf", "r") as conf_file: 
                
                conf_file_list = conf_file.readlines()
                window.geometry(conf_file_list[0].rstrip('\n'))
                
                theme_name = conf_file_list[1].split('+')[0]
                font_name = conf_file_list[1].split('+')[1]
                font_size = int(conf_file_list[1].split('+')[2])
                font_style = conf_file_list[1].split('+')[3]
                
                text.configure(font=(font_name, font_size, font_style))
                on_menu_set_theme(theme_name)
        
        except:
            print('[ERROR]: Config file is invalid!')
            set_window_default_geometry()

    else:
        set_window_default_geometry()


def on_close():
     
    if not is_saved:
        answer_on_exit = askyesno(title='EXIT', message='Exit the program without saving?', icon = QUESTION)
        close = answer_on_exit
        
        if close:            
            save_window_geometry()
            window.destroy()
    
    else:
        save_window_geometry()
        window.destroy()

# --->


# <--- File menu
def on_menu_open_file():
    
    global is_saved
    global is_modified
    global file_name
    
    if is_modified == True:
        
        showwarning('WARNING', 'Save current file before opening another file!')
    
    else:
        file_name = fd.askopenfilename()

        file = open(file_name, 'r', encoding = 'utf-8')
        file_string = file.read()
        text.delete(1.0, END)
        text.insert(1.0, file_string)
        file.close()
        window.title(file_name+' - '+prog_name+prog_version)

        is_saved = True
        is_modified = False


def on_menu_save_as_file():
    
    global is_saved
    global is_modified
    global file_name

    file_name = fd.asksaveasfilename(filetypes = (('txt', '*.txt'), 
                                                  ('conf', '*.conf'),
                                                  ('ini', '*.ini'),
                                                  ('json', '*.json'),
                                                  ('xml', '*.xml'),
                                                  ('Anything', '*.*')),
                                    defaultextension='.txt')
    
    if file_name:

        file = open(file_name, 'w', encoding = 'utf-8')
        file_string = text.get(1.0, 'end-1c')
        file.write(file_string)
        file.close()
        window.title(file_name+' - '+prog_name+prog_version)
        is_saved = True
        is_modified = False


def on_menu_save_file():
    
    global is_saved
    global file_name
    global is_modified

    if is_saved == False and file_name == '':
        on_menu_save_as_file()

    elif is_saved == False and file_name != '':
        file = open(file_name, 'w', encoding = 'utf-8')
        file_string = text.get(1.0, 'end-1c')
        file.write(file_string)
        file.close()

        is_saved = True
        is_modified = False

# --->


# <--- Theme menu
def on_menu_set_theme(theme_str: str):
    
    global theme_name

    theme_list = {
        'Light': ['black', 'white', 'black'],
        'Black and White': ['white', 'black', 'white'],
        'Cyberpunk': ['#00c2a2', '#25022d', 'red'],
        'Cybperunk Raspberry': ['#f1136e', 'black', 'red']
    }

    if theme_str == 'Light':

        text.configure(foreground = theme_list['Light'][0], 
                       background = theme_list['Light'][1], 
                       insertbackground = theme_list['Light'][2])
        theme_name = theme_str
    
    elif theme_str == 'Black and White':

        text.configure(foreground = theme_list['Black and White'][0], 
                       background = theme_list['Black and White'][1], 
                       insertbackground = theme_list['Black and White'][2])
        theme_name = theme_str
    
    elif theme_str == 'Cyberpunk':

        text.configure(foreground = theme_list['Cyberpunk'][0], 
                       background = theme_list['Cyberpunk'][1], 
                       insertbackground = theme_list['Cyberpunk'][2])
        theme_name = theme_str

    elif theme_str == 'Cyberpunk Raspberry':

        text.configure(foreground = theme_list['Cybperunk Raspberry'][0], 
                       background = theme_list['Cybperunk Raspberry'][1], 
                       insertbackground = theme_list['Cybperunk Raspberry'][2])
        theme_name = theme_str

# --->


# <--- Format menu
def on_menu_set_font_size(modifier: str):
    
    global font_size
    global font_name
    global font_style

    if modifier == '+':
        text.configure(font=(font_name, font_size+1, font_style))
        font_size +=1

    elif modifier == '-':
        text.configure(font=(font_name, font_size-1, font_style))
        font_size -=1


def on_menu_set_font_style(style_str: str):

    global font_size
    global font_name
    global font_style

    if style_str == 'normal':
        text.configure(font=(font_name, font_size, 'normal'))
        font_style = 'normal'
    
    elif style_str == 'bold':
        text.configure(font=(font_name, font_size, 'bold'))
        font_style = 'bold'

    elif style_str == 'italic':
        text.configure(font=(font_name, font_size, 'italic'))
        font_style = 'italic'

def on_menu_reset_font_size_style():

    global font_size
    global font_name
    global font_style

    text.configure(font=('Courier', 11, 'normal'))

    font_size = 11
    font_style = 'normal'


def on_menu_show_font_settings_window():
    
    font_settings_window = Toplevel()
    font_settings_window.title('Font settings')
    font_settings_window.resizable(False, False)
    font_settings_window.focus()

    font_settings_window_w = 250
    font_settings_window_h = 150
    screen_w = font_settings_window.winfo_screenwidth()
    screen_h = font_settings_window.winfo_screenheight()
    x = (screen_w/2) - (font_settings_window_w/2)
    y = (screen_h/2) - (font_settings_window_h/2)
    font_settings_window.geometry('%dx%d+%d+%d' % (font_settings_window_w, font_settings_window_h, x, y))

    font_increase_button = Button(master=font_settings_window, width=16, height=1, text='Bigger (+1)', command= lambda: on_menu_set_font_size('+'))
    font_decrease_button = Button(master=font_settings_window, width=16, height=1, text='Smaller (-1)', command= lambda: on_menu_set_font_size('-'))

    font_size_label = Label(master=font_settings_window, text='Font size')
    font_style_label = Label(master=font_settings_window, text='Font style')

    font_style_list = [('Normal', 'normal'), 
                       ('Bold', 'bold'),
                       ('Italic', 'italic')]

    font_size_label.pack()
    font_increase_button.pack(padx= 5, pady= 5)
    font_decrease_button.pack(padx= 5, pady= 5)
    font_style_label.pack()

    font_style_selected = StringVar()
    
    font_style_radiobutton_normal = Radiobutton(master = font_settings_window, 
                                                text=font_style_list[0][0], 
                                                value=font_style_list[0][1], 
                                                variable= font_style_selected, 
                                                command= lambda: on_menu_set_font_style(font_style_list[0][1]))
    font_style_radiobutton_bold = Radiobutton(master = font_settings_window, 
                                              text=font_style_list[1][0], 
                                              value=font_style_list[1][1], 
                                              variable= font_style_selected, 
                                              command= lambda: on_menu_set_font_style(font_style_list[1][1]))
    font_style_radiobutton_italic = Radiobutton(master = font_settings_window, 
                                                text=font_style_list[2][0], 
                                                value=font_style_list[2][1], 
                                                variable= font_style_selected, 
                                                command= lambda: on_menu_set_font_style(font_style_list[2][1]))
    
    font_style_radiobutton_normal.pack(side=LEFT, padx=10)
    font_style_radiobutton_bold.pack(side=LEFT, padx=10)
    font_style_radiobutton_italic.pack(side=LEFT, padx=10)

# --->


# <--- About menu
def show_about_window():

    about_window = Toplevel()
    about_window.overrideredirect(True) # Window has no title
    about_window.focus()

    about_window_w = 250
    about_window_h = 150
    screen_w = about_window.winfo_screenwidth()
    screen_h = about_window.winfo_screenheight()
    x = (screen_w/2) - (about_window_w/2)
    y = (screen_h/2) - (about_window_h/2)
    about_window.geometry('%dx%d+%d+%d' % (about_window_w, about_window_h, x, y))

    about_label = Label(master=about_window, text='About Aurora Text Editor')
    about_label.pack(side=TOP)

    about_info_label = Label(master=about_window, text='Minimalistic text editor.\nCreated with Python and Tkinter.\n\nThank you for using this program!', relief='solid', padx=20, pady=10)
    about_ok_button = Button(master=about_window, text='OK', command= lambda: about_window.destroy())
    
    about_ok_button.pack(side=BOTTOM)
    about_info_label.pack(side=TOP)

# --->


# <--- Menubar and Menus
# Menubar
main_menu = Menu(master=window)
window.config(menu=main_menu)

# File
file_menu = Menu(main_menu, tearoff=False)
main_menu.add_cascade(label="File", menu = file_menu)
file_menu.add_command(label="Open file", command = on_menu_open_file)
file_menu.add_command(label="Save file", command = on_menu_save_file)
file_menu.add_command(label="Save file as", command = on_menu_save_as_file)
file_menu.add_command(label="Exit", command = on_close)

# Format
format_menu = Menu(main_menu, tearoff=False)
main_menu.add_cascade(label="Format", menu = format_menu)
format_menu.add_command(label="Font settings", command=on_menu_show_font_settings_window)
format_menu.add_separator()
format_menu.add_command(label="Reset Font size and style", command=on_menu_reset_font_size_style)

# Theme
theme_menu = Menu(main_menu, tearoff=False)
main_menu.add_cascade(label="Theme", menu = theme_menu)
theme_menu.add_command(label="Light", command = lambda: on_menu_set_theme('Light'))
theme_menu.add_command(label="Black and White", command = lambda: on_menu_set_theme('Black and White'))
theme_menu.add_command(label="Cyberpunk", command = lambda: on_menu_set_theme('Cyberpunk'))
theme_menu.add_command(label="Cyberpunk Raspberry", command = lambda: on_menu_set_theme('Cyberpunk Raspberry'))

# Context Menu
context_menu = Menu(text, tearoff=False)
context_menu.add_command(label="Copy")
context_menu.add_command(label="Paste")
context_menu.add_command(label="Cut")
context_menu.add_separator()
context_menu.add_command(label="Select all")

def context_menu_select_all(event = None):
    text.tag_add('sel', 1.0, 'end-1c')
    return 'break'

def context_menu_show(event):
    context_menu.entryconfigure("Copy", command = lambda: text.event_generate("<<Copy>>"))
    context_menu.entryconfigure("Paste", command = lambda: text.event_generate("<<Paste>>"))
    context_menu.entryconfigure("Cut", command = lambda: text.event_generate("<<Cut>>"))
    context_menu.entryconfigure("Select all", command = context_menu_select_all)
    context_menu.tk.call("tk_popup", context_menu, event.x_root, event.y_root)

# About
about_menu = Menu(main_menu, tearoff=False)
main_menu.add_cascade(label="?", menu = about_menu)
about_menu.add_command(label="About", command=show_about_window)
# --->


# <--- Run all service functions before the program starts
on_start()
status_bar_info()
text.bind('<Key>', is_modified_text_event)
text.bind('<Button-3><ButtonRelease-3>', context_menu_show)
text.bind('<Control-a>', context_menu_select_all)
# --->


# <--- Main functions to execute program
window.protocol('WM_DELETE_WINDOW', on_close)
window.mainloop()
# --->
