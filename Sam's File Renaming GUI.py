
import tkinter as tk
from tkinter import filedialog as tkf
from tkinter import simpledialog
import os
import re


'''
TO DO--------------------------------------

HIGH--------------------------------------
window resizing
sub folders check box

MEDIUM--------------------------------------
error catching for input strings
file check boxes / applying edits to selected files

LOW--------------------------------------
aesthetics
more error handling?

NICE TO HAVE--------------------------------------
Folder empty message
make old file names not editable
file type icons
object oriented programming

DONE--------------------------------------
exclude folders
user input pop up boxes
general error handling e.g. when file fails to rename
make clear button disappear when not populated?
loop through dictionary for tv renamer
'''


class attrdict(dict):
    # dot.notation access to dictionary attributes
    __getattr__ = dict.get
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__


def rgb_tk(rgb):
    # translates an rgb tuple of int to a tkinter friendly color code
    return "#%02x%02x%02x" % rgb


def is_part(some_string, target):
    return target in some_string


def file_name(fln):  # finds the name part of a file name without the extension
    return fln[:-(len(fln) - fln.rfind("."))]


def file_ext(fle):  # finds just the extension e.g. .mkv
    return fle[-(len(fle) - fle.rfind(".")):]


def snip_text_after(str, fnd):  # snips text after and including fnd
    if is_part(str, fnd):
        return str[: str.rfind(fnd)]
    else:
        return str


def snip_text_before(str, fnd):  # snips text before and including fnd
    if is_part(str, fnd):
        return str[str.rfind(fnd) + len(fnd):]
    else:
        return str


def snip_end(input_string, chars):
    return input_string[:-chars]


def snip_start(input_string, chars):
    return input_string[chars:]


def name_cleaner_tv(nmc):

    tv = nmc
    tv = tv.lower()  # lowercase for ease of search/replace
    tv = tv.replace('.', ' ')  # replace period with space
    tv = tv.replace('_', ' ')  # replace underscore with space
    for x in [' 1080p', ' 720p', ' 2160p']:
        tv = snip_text_after(tv, x)
    tv = tv.replace('repack', '')  # delete repack
    tv = tv.replace('remastered', '')  # delete remastered
    for x in range(3):
        tv = tv.replace('  ', ' ')  # delete double spaces
    if tv.endswith(' '):
        tv = tv[:-1]
    tv = tv.title()  # Title case
    tv = tv.replace("'S", "'s")  # replace underscore with space
    for x in ['St', 'Nd', 'Rd', 'Th']:  # 1st 2nd 3rd 4th etc
        tv = re.sub(r'(?<=[0-9]){0}'.format(x), x.lower(), tv)
    short_words = "of an and for by is from etc a to the".split()
    for x in short_words:  # lowercase short words in middle of name
        tv = tv.replace(' ' + x.title() + ' ', ' ' + x + ' ')
    for x in short_words:  # lowercase short words at start of name
        tv = re.sub(f'(?<=S[0-9][0-9]E[0-9][0-9] ){x}', x.title(), tv)
    return tv


def name_cleaner_movieyear(movie_name):
    mv = movie_name
    mv = mv[:len(mv) - 4] + '[' + mv[len(mv) - 4:]
    mv = mv + ']'
    return mv


def dialog_find():
    find_str = simpledialog.askstring('Find', 'String to find (case sensitive).', parent=win)
    replace_str = simpledialog.askstring('Replace', 'Replacement string (case sensitive). Leave blank to delete string from file names.', parent=win)
    edit_ents(lambda y: y.replace(find_str, replace_str))


def dialog_generic(dialog_title, dialog_text, dialog_function):
    global dialog_input
    dialog_input = simpledialog.askstring(dialog_title, dialog_text, parent=win)
    edit_ents(dialog_function)


# set up file lists and stuff
# ==================================================================
# dtry = os.listdir("C:\Users\Sam\Documents\myPython")
# dtry = os.listdir("C:\Users\Sam\Downloads")


default_folder = ''
# below if block assigns default folder to my testing folder if samgf is the user
if os.getenv('username') == 'samgf':
    default_folder = r'C:\Users\samgf\OneDrive\Documents\my_python\Testing\Testing'
else:
    default_folder = ''


log_separator = '-----complete.'
total_files_limit = 100
dtry = []
fldr = ''

colors = {
    'green': rgb_tk((200, 255, 200)),
    'red': rgb_tk((255, 185, 170)),
    'purple': rgb_tk((235, 185, 255)),
    'grey_light': rgb_tk((250, 250, 250)),
    'cyan': rgb_tk((150, 230, 255)),
    'blue_light': rgb_tk((220, 240, 255))
    }


col = {
    'dir': 0,
    'old': 1,
    'new': 2,
    'ext': 3
    }

col = attrdict(col)


def load_dtry(fldr):
    dtry[:] = []  # clear list
    global root_dtry
    root_dtry = fldr

    def get_all_folder_paths(dir):
        result = []
        for root, dirs, files in os.walk(dir):
            result.extend([root for f in files])
        return result

    def get_all_files(dir):
        result = []
        for root, dirs, files in os.walk(dir):
            result.extend(files)
        return result

    def get_all_file_paths(dir):
        result = []
        for root, dirs, files in os.walk(dir):
            result.extend([os.path.join(root, f) for f in files])
        return result

    dtry.append(get_all_folder_paths(fldr))
    for i in range(3):
        dtry.append(get_all_files(fldr))

    # change the lists:
    # old file name list without extension
    for i, name in enumerate(dtry[col.old]):
        dtry[col.old][i] = file_name(dtry[col.old][i])
    # new file name list without extension
    for i, name in enumerate(dtry[col.new]):
        dtry[col.new][i] = file_name(dtry[col.new][i])
    # list of extensions for files
    for i, name in enumerate(dtry[col.ext]):
        dtry[col.ext][i] = file_ext(dtry[col.ext][i])


def replace_entry_text(an_entry, some_text):
    an_entry.delete(0, tk.END)
    an_entry.insert(tk.END, some_text)


title_text = "Sam's File Renamer"


win = tk.Tk()  # create instance
win.title(title_text)  # add title to GUI
win.configure(bg=colors['blue_light'])
# win.geometry('800x120')  # GUI size
'''
def sizer():
    win.update_idletasks()
    width = win.winfo_width()
    height = win.winfo_height()
    x = (win.winfo_screenwidth() // 2) - (width // 2)
    y = (win.winfo_screenheight() // 2) - (height // 2)
    # win.geometry('f{width}x{height}+{x}+{y}')
    win.geometry('{}x{}+{}+{}'.format(win.winfo_width(), win.winfo_height(), x, y))
'''


def win_position(wn, x, y):
    wn.geometry(f'+{x}+{y}')


def win_centre(wn):
    offset = - 170
    x = (wn.winfo_screenwidth() // 2) - (wn.winfo_width() // 2)
    y = (wn.winfo_screenheight() // 2) - (wn.winfo_height() // 2)
    win_position(wn, x + offset, y + offset)


win_centre(win)

# win.resizable(False, False)
win.iconbitmap('Document.ico')  # icon in top left


# /=================================================================

# intro frame including: intro text widget, folder entry
# ==================================================================


fr_intro = tk.Frame(win, bg=colors['blue_light'])
fr_intro.pack(side=tk.TOP, pady=10, anchor="w")

# intro text
lbl_intro = tk.Label(fr_intro, text='Browse for a folder, then click populate to get started.', bg=colors['blue_light'])
lbl_intro.grid(row=0, column=0)

# folder name Entry box
ent_folder = tk.Entry(fr_intro)
ent_folder.bind("<Return>", (lambda event: populate_button()))
ent_folder.insert(tk.END, str(default_folder))
ent_folder.grid(row=1, column=0)


def browse_button():
    print("Browse!")
    brse = tkf.askdirectory()
    replace_entry_text(ent_folder, brse)


# /=================================================================

# file frame, lists
# ==================================================================
fr_files = tk.Frame(win, bg=colors['blue_light'])
fr_files.pack(side=tk.BOTTOM, fill="both", expand=True)
'''
fr_files.grid_columnconfigure(0, weight=3)
fr_files.grid_columnconfigure(1, weight=3)
fr_files.grid_columnconfigure(2, weight=1)
'''

files_start_row = 1
ents = [[], [], []]
titles_widgets = []
# /=================================================================


def rename_files():
    def renamer(directory, oldname, newname, extension):
        os.rename(os.path.join(directory.get(), oldname.get() + extension.get()),
                  os.path.join(directory.get(), newname.get() + extension.get())),
        replace_entry_text(oldname, newname.get())
    print('Renaming-----')
    print("Root Directory: " + root_dtry)
    for i, name in enumerate(ents[col.old]):
        subdirectory = ents[col.dir][i].get()
        old_full_name = ents[col.old][i].get() + ents[col.ext][i].get()
        new_full_name = ents[col.new][i].get() + ents[col.ext][i].get()
        print(subdirectory + " | " + old_full_name + " -> " + new_full_name, end=" ")

        def ents_row_colour(rgb_inp):
            for c in range(0, 4):
                ents[c][i].configure(bg=rgb_inp)
        try:
            renamer(ents[col.dir][i], ents[col.old][i], ents[col.new][i], ents[col.ext][i])
            ents_row_colour(colors['green'])
            print("| pass")
        except FileNotFoundError:
            print("| file not found")
            ents_row_colour(colors['red'])
        except OSError:
            print("| invalid file name, ")
            ents_row_colour(colors['cyan'])
        except PermissionError:
            print("| permission error")
            ents_row_colour(colors['purple'])
    print(log_separator)


def populate():
    for x in ents:
        for y in x:
            y.destroy()

    Buttons['clear']['widget'].grid(row=Buttons['clear']['row'], column=1)

    ents[:] = []  # clear list

    # make 4 identical file lists within ents
    for i in range(4):
        ents.append([])

    load_dtry(ent_folder.get())  # update dtry with current folder address

    for i, num in enumerate([1000, 1000, 1000, 1]):
        fr_files.grid_columnconfigure(i, weight=num)

    # title row
    title_row = ["Folder", "Old File Name", "New File Name", "Extension"]
    for t in range(len(title_row)):
        title_label = tk.Label(fr_files, bg=colors['blue_light'], text=title_row[t])
        title_label.grid(row=1, column=t, sticky=tk.W)  # , columnspan=colconfig[t])

        titles_widgets.append(title_label)  # add title to titles widget list

    for x in range(len(title_row)):
        # columns for files
        for i, name in enumerate(dtry[x]):  # loop through all files in each sublist of dtry
            ent = tk.Entry(fr_files)  # , sticky=1)  # width=38)  # set up widget 2
            ent.insert(tk.END, str(name))  # add text to widget
            ent.grid(row=i + 1 + files_start_row, column=x, sticky=tk.W + tk.E)  # , columnspan=colconfig[x])  # place widget on grid

            # print(colconfig[x])
            ents[x].append(ent)  # add widget to ents list

    Buttons['rename all']['widget'].grid(row=2, column=0)
    # OLD LOCATION IN fr_files Buttons['rename all']['widget'].grid(row=files_start_row + len(dtry[col.dir]) + 1, column=0, pady=10)


def populate_button():  # populate file columns and buttons
    print("Populate-----")
    try:
        total_files = sum([len(files) for r, d, files in os.walk(ent_folder.get())])
        if 0 < total_files <= total_files_limit:
            print(f'Folder has {total_files} files inside. Writing to window...')
            populate()
        elif total_files == 0:
            print('Folder has no files inside')
        elif total_files > total_files_limit:
            print(f'Folder (incuding subfolders) has {total_files} files inside which exceeds the limit of {total_files_limit}. Functionality has not been added yet to handle this many files')
        else:
            print('Unspecified folder error')
    except StopIteration:
        print("Error, folder does not exist")

    print(log_separator)


def clear_files():
    print('Clear file list from window-----')
    for x in titles_widgets:
        x.grid_remove()

    for x in ents:
        for y in x:
            y.grid_remove()

    Buttons['rename all']['widget'].grid_remove()  # _forget()
    Buttons['clear']['widget'].grid_remove()

    print(log_separator)


# /=================================================================

# some buttons
# ==================================================================

# set up rename button but do not pack
Buttons = {
    'populate': {
        'command': populate_button,
        'row': 0,
        'column': 1,
        'grid_on_start': True,
        'bg': 'white'
        },
    'browse': {
        'command': browse_button,
        'row': 1,
        'column': 1,
        'grid_on_start': True,
        'bg': 'white'
        },
    'clear': {
        'command': clear_files,
        'row': 2,
        'column': 1,
        'grid_on_start': False,
        'bg': colors['red']
        },
    'rename all': {
        'command': rename_files,
        'row': 2,
        'column': 0,
        'grid_on_start': False,
        'bg': colors['green']
        }
    }

for k in Buttons:
    Buttons[k]['widget'] = tk.Button(fr_intro, text=k.capitalize(), command=Buttons[k]['command'], bg=Buttons[k]['bg'])
    if Buttons[k]['grid_on_start']:
        Buttons[k]['widget'].grid(row=Buttons[k]['row'], column=Buttons[k]['column'], pady=3)


# /=================================================================

# create menu
# ==================================================================


def edit_ents(some_function):
    # apply inputted function to new file name list
    for i, name in enumerate(ents[col.new]):
        ent_text = ents[col.new][i].get()
        ent_text = some_function(ent_text)
        replace_entry_text(ents[col.new][i], ent_text)


def donothing():
    pass


menu = tk.Menu(win)  # add menu
win.config(menu=menu)  # config menu

# set up menu tabs
menu_tabs = {}
for x in ['file', 'case', 'snip', 'downloads', 'other']:
    menu_tabs[x] = tk.Menu(menu, tearoff=0)  # create tabs
for k, v in menu_tabs.items():
    menu.add_cascade(label=k.title(), menu=v)  # add tabs

# info for all of the commands to be added to the various menu tabs
Menu_Commands = {
    # file
    'exit': {
        'menu': menu_tabs['file'],
        'title': 'Exit',
        'dialog': False,
        'command': lambda: win.destroy()
        },
    # case
    'uppercase': {
        'menu': menu_tabs['case'],
        'title': 'UPPERCASE',
        'dialog': False,
        'command': lambda: edit_ents(lambda x: x.upper())
        },
    'lowercase': {
        'menu': menu_tabs['case'],
        'title': 'lowercase',
        'dialog': False,
        'command': lambda: edit_ents(lambda x: x.lower())
        },
    'title_case': {
        'menu': menu_tabs['case'],
        'title': 'Title Case',
        'dialog': False,
        'command': lambda: edit_ents(lambda x: x.title())
        },
    'sentence_case': {
        'menu': menu_tabs['case'],
        'title': 'Sentence case',
        'dialog': False,
        'command': lambda: edit_ents(lambda x: x.capitalize())
        },
    # downloads
    'download_sorter': {
        'menu': menu_tabs['downloads'],
        'title': 'Download Sorter',
        'dialog': False,
        'command': lambda: edit_ents(name_cleaner_tv)
        },
    'movie_year': {
        'menu': menu_tabs['downloads'],
        'title': 'Movie Year',
        'dialog': False,
        'command': lambda: edit_ents(
            name_cleaner_movieyear)
        },
    # snip
    'snip_before': {
        'menu': menu_tabs['snip'],
        'title': 'Snip text before x',
        'text': 'Snip text before and including input string',
        'dialog': True,
        'command': lambda y: snip_text_before(y, dialog_input)
        },
    'snip_after': {
        'menu': menu_tabs['snip'],
        'title': 'Snip text after x',
        'text': 'Snip text after and including input string',
        'dialog': True,
        'command': lambda y: snip_text_after(y, dialog_input)
        },
    'snip_start': {
        'menu': menu_tabs['snip'],
        'title': 'Snip x chars from start',
        'text': 'Snip x characters from start of name',
        'dialog': True,
        'command': lambda y: snip_start(y, int(dialog_input))
        },
    'snip_end': {
        'menu': menu_tabs['snip'],
        'title': 'Snip x chars from end',
        'text': 'Snip x characters from end of name',
        'dialog': True,
        'command': lambda y: snip_end(y, int(dialog_input))
        },
    # other
    'replace': {
        'menu': menu_tabs['other'],
        'title': 'Replace x with y',
        'dialog': False,
        'command': dialog_find
        },
    'prefix': {
        'menu': menu_tabs['other'],
        'title': 'Prefix',
        'text': 'Prefix to be added to file names (including spaces, dashes underscores etc.)',
        'dialog': True,
        'command': lambda y: dialog_input + y
        },
    'suffix': {
        'menu': menu_tabs['other'],
        'title': 'Suffix',
        'text': 'Suffix to be added to file names (including spaces, dashes underscores etc.)',
        'dialog': True,
        'command': lambda y: y + dialog_input
        }
    }

# loop through the Menu_Commands dic and add commands using the info
for key in Menu_Commands:  # add command with user input
    if 'text' in Menu_Commands[key]:
        Menu_Commands[key]['menu'].add_command(label=Menu_Commands[key]['title'], command=lambda title=Menu_Commands[key]['title'], text=Menu_Commands[key]['text'], command=Menu_Commands[key]['command']: dialog_generic(title, text, command))
    else:  # add generic command
        Menu_Commands[key]['menu'].add_command(label=Menu_Commands[key]['title'], command=Menu_Commands[key]['command'])

# /=================================================================

# run mainloop
# ==================================================================

win.mainloop()  # start GUI / create the main loop
