from customwidgets import *
from typing import Any, Literal
from customtkinter import (CTk, CTkToplevel, CTkFrame, CTkLabel, CTkEntry, CTkButton, CTkTextbox, END, WORD, CTkFont,
                           Variable, CTkImage, IntVar)
from crypto import *
from tkinter.ttk import Treeview as TtkTreeview
from tkinter import filedialog, messagebox, Misc
import os
import sys
import pyperclip

DEFAULT_ROOT_FG = 'black'
DEFAULT_FRAME_FG = '#1c0016'
DEFAULT_WIDGET_FG = '#4a0064'
DEFAULT_BUTTON_FG = '#650089'
DEFAULT_BUTTON_HOVER_FG = '#46004c'
DEFAULT_TEXTCOLOR = '#ffffff'
DEFAULT_TEXTCOLOR_DISABLED = '#818181'
DEFAULT_TEXTCOLOR_PLACEHOLDER = DEFAULT_TEXTCOLOR_DISABLED
DEFAULT_BORDER_COLOR = '#4c4c4c'
DEFAULT_BORDERWIDTH = 1
FONT_NORMAL = ('Arial', 12)
FONT_BIG = ('Arial', 18)


# DisplayWindow: classmethod
# MainWindow: classmethod
# InfoWindow: classmethod
# FirstUseWindow: classmethod


def browse_dirs(entry: Entry):
    selected_dir = filedialog.askdirectory(title='Select directory')
    if selected_dir:
        entry.configure(state='normal')
        entry.delete(0, END)
        entry.insert(0, selected_dir)
        entry.configure(state='disabled')


def set_focus_by_index(index_var: IntVar, widget_dict: dict, *args):
    index = index_var.get()
    widget_to_focus_in = widget_dict.get(index)
    widget_to_focus_in.focus_set()

    if index == len(widget_dict):
        index_var.set(1)
    else:
        index_var.set(index + 1)

    return "break"  # stops tkinter from calling default behaviour after '<Tab>' event


def set_binds_buttons(button: CTkButton, command: () = None):
    button.bind('<FocusIn>', lambda event: button.configure(fg_color=DEFAULT_BUTTON_HOVER_FG))
    button.bind('<FocusOut>', lambda event: button.configure(fg_color=DEFAULT_BUTTON_FG))
    if command:
        button.bind('<Return>', lambda event: command())


class MainWindow:
    def __init__(self, master: CTk, info_window: "InfoWindow", display_window: "DisplayWindow",
                 first_use_window: "FirstUseWindow", ):
        self.root = master

        self.info_window_obj = info_window
        self.display_window_obj = display_window
        self.first_use_obj = first_use_window

        # This might cause issues when switching between windows, but if this bind is applied to the frame, it at first
        # sets focus on the entry, and after second input calls right method
        self.root.bind('<Tab>', lambda event: set_focus_by_index(self.tab_focus_index, self.widget_dict))
        self.root.bind('<Escape>', lambda event: sys.exit())

        self.main_frame = Frame(master=self.root)

        self.title_label = Label(master=self.main_frame,
                                 text='Welcome',
                                 font=FONT_BIG)

        hide_character = StringVar(value='*')
        self.key_entry = Entry(master=self.main_frame,
                               placeholder_text='Enter key',
                               width=350,
                               show=hide_character.get())
        self.key_entry.bind('<Return>', self.display_init)
        self.key_entry.bind('<FocusIn>', lambda event: self.keyboard_current_focus.set(1))

        self.show_key_checkbox = CensorCheckbox(master=self.main_frame, entry=self.key_entry, str_var=hide_character)

        self.info_button = Button(master=self.main_frame,
                                  text='?',
                                  width=30,
                                  height=5,
                                  command=self.info_init)
        set_binds_buttons(button=self.info_button, command=self.info_init)

        self.first_use_button = Button(master=self.main_frame,
                                       text='First use',
                                       command=self.first_use_init)
        set_binds_buttons(button=self.first_use_button, command=self.first_use_init)

        self.confirm_button = Button(master=self.main_frame,
                                     text='Confirm',
                                     command=self.display_init)
        set_binds_buttons(button=self.confirm_button, command=self.display_init)

        self.widget_dict = {1: self.key_entry,
                            2: self.confirm_button,
                            3: self.first_use_button,
                            4: self.info_button}

        self.keyboard_current_focus = IntVar(value=1)  # integer related to the right widget in self.widget_dict
        self.tab_focus_index = IntVar(value=1)

        self.keyboard_frame = KeyboardFrame(master=self.root,
                                            write_on=self.widget_dict[self.keyboard_current_focus.get()])

        self.title_label.grid(row=0, column=0, columnspan=3, padx=5, pady=(5, 0))
        self.key_entry.grid(row=1, column=0, columnspan=2, padx=5, pady=(5, 0))
        self.show_key_checkbox.grid(row=1, column=2, padx=5, pady=(5, 0))
        self.info_button.grid(row=0, column=0, sticky='nw', padx=5, pady=(5, 0))
        self.first_use_button.grid(row=2, column=0, columnspan=3, padx=5, pady=(5, 5), sticky='w')
        self.confirm_button.grid(row=2, column=0, columnspan=3, padx=5, pady=(5, 5), sticky='e')
        self.main_frame.place(relx=0.5, rely=0.5, anchor='center')
        self.keyboard_frame.place(relx=0.5, rely=0.99, anchor='s')

    def info_init(self, *args):
        raise NotImplementedError

    def first_use_init(self, *args):
        self.first_use_obj.first_use_frame.lift()
        self.main_frame.lower()
        self.keyboard_frame.change_linked_widget(self.first_use_obj.widget_dict[self.first_use_obj.keyboard_current_focus.get()])
        self.root.bind('<Tab>', lambda event: set_focus_by_index(self.first_use_obj.tab_focus_index, self.first_use_obj.widget_dict))

    def display_init(self, *args):
        raise NotImplementedError

    # look main.py for explaination
    def update_objects(self, new_first_use_obj: "FirstUseWindow", new_info_window_obj: "InfoWindow",
                       new_display_window_obj: "DisplayWindow"):
        self.first_use_obj = new_first_use_obj
        self.info_window_obj = new_info_window_obj
        self.display_window_obj = new_display_window_obj

    def exit(self, *args):
        self.main_frame.destroy()


class InfoWindow:
    def __init__(self):
        pass


class FirstUseWindow:
    def __init__(self, master: CTk, main_window: MainWindow):
        self.root = master

        self.first_use_frame = Frame(master=self.root)

        self.main_window_obj = main_window
        self.keyboard_frame = main_window.keyboard_frame
        hide_character = StringVar(value='*')

        self.title_label = Label(master=self.first_use_frame,
                                 text='Setup',
                                 font=FONT_BIG)

        self.key_entry = Entry(master=self.first_use_frame,
                               placeholder_text='Enter the key',
                               width=325,
                               show=hide_character.get())
        self.key_entry.insert(0, generate_key())
        self.key_entry.bind('<FocusIn>', lambda event: self.keyboard_current_focus.set(1))

        self.show_key_checkbox = CensorCheckbox(master=self.first_use_frame,
                                                entry=self.key_entry,
                                                str_var=hide_character)

        self.copy_key_button = Button(master=self.first_use_frame,
                                      text='Copy',
                                      width=66,
                                      command=lambda: pyperclip.copy(self.key_entry.get()))
        set_binds_buttons(button=self.copy_key_button, command=lambda: pyperclip.copy(self.key_entry.get()))

        self.directory_entry = Entry(master=self.first_use_frame,
                                     placeholder_text='Select directory',
                                     width=325,
                                     state='normal')
        self.directory_entry.configure(state='disabled')
        self.directory_entry.bind('<Button-1>', lambda event: browse_dirs(entry=self.directory_entry))

        self.browse_dirs_button = Button(master=self.first_use_frame,
                                         text='Browse',
                                         width=66,
                                         command=lambda: browse_dirs(entry=self.directory_entry))
        set_binds_buttons(button=self.browse_dirs_button, command=lambda: browse_dirs(entry=self.directory_entry))

        self.exit_button = Button(master=self.first_use_frame,
                                  text='Exit',
                                  command=self.exit)
        set_binds_buttons(button=self.exit_button, command=self.exit)

        self.confirm_button = Button(master=self.first_use_frame,
                                     text='Confirm',
                                     command=self.confirm)
        set_binds_buttons(button=self.confirm_button, command=self.confirm)

        self.widget_dict = {1: self.key_entry,
                            2: self.copy_key_button,
                            3: self.browse_dirs_button,
                            4: self.confirm_button,
                            5: self.exit_button}

        self.tab_focus_index = IntVar(value=1)
        self.keyboard_current_focus = IntVar(value=1)

        self.title_label.grid(row=0, column=0, columnspan=3, pady=(5, 1), padx=5)
        self.key_entry.grid(row=1, column=0, pady=1, padx=5)
        self.copy_key_button.grid(row=1, column=1, pady=1, padx=5)
        self.show_key_checkbox.grid(row=1, column=2, pady=1, padx=5)
        self.directory_entry.grid(row=2, column=0, pady=1, padx=5)
        self.browse_dirs_button.grid(row=2, column=1, pady=1, padx=5)
        self.confirm_button.grid(row=3, column=0, columnspan=3, sticky='e', pady=(10, 5), padx=5)
        self.exit_button.grid(row=3, column=0, columnspan=3, sticky='w', pady=(10, 5), padx=5)
        self.first_use_frame.place(relx=0.5, rely=0.5, anchor='center')
        self.first_use_frame.lower()

    def confirm(self):
        if not messagebox.askyesno('Confirmation', 'After finishing this configuration you will no'
                                                   ' longer be able to get access to the key and initialization'
                                                   ' vector, which will be necessary to later decrypt the'
                                                   ' source file.\nAre you sure you wand to end the'
                                                   ' configuration?'):
            return

        user_key = self.key_entry.get()
        user_dir = self.directory_entry.get()

        if not user_key:
            messagebox.showerror('Error', "Key wasn't provided.")
            return

        elif not user_dir:
            messagebox.showerror('Error', "Directory wasn't selected.")
            return

        elif not os.path.isdir(user_dir):
            messagebox.showerror('Error', "Selected directory doesn't exist.")
            return

        if os.path.exists(fr'{user_dir}\src'):
            additional_number = 1
            while os.path.exists(fr'{user_dir}\src ({additional_number})'):
                additional_number += 1
            name_of_source_file = f'src ({additional_number})'
        else:
            name_of_source_file = 'src'

        print(f'User key initial: {user_key}')
        print(f'Length of the provided key: {len(user_key)}')
        if not len(user_key) == 48:
            if len(user_key) < 48:
                user_key = f'{user_key:a<48}'
                print(f'Too short, new key: {user_key}')
            else:
                user_key = user_key[:48]
                print(f'Too long,  new key: {user_key}')
            print(f'New key length: {len(user_key)}')

        user_key_bytes = user_key.encode()

        validation_str = 'Beautiful is better than ugly.'
        validation_str_encrypted = encrypt_str(validation_str, user_key_bytes)

        with open(fr'{user_dir}\{name_of_source_file}', 'xb') as file:
            file.write(validation_str_encrypted + b'<SEPARATOR>')

        self.exit()

    def exit(self):
        self.main_window_obj.main_frame.lift()
        self.first_use_frame.lower()
        self.main_window_obj.keyboard_frame.change_linked_widget(self.main_window_obj.widget_dict[self.main_window_obj.keyboard_current_focus.get()])
        self.root.bind('<Tab>', lambda event: set_focus_by_index(self.main_window_obj.tab_focus_index,
                                                                 self.main_window_obj.widget_dict))


class DisplayWindow:
    def __init__(self):
        pass
