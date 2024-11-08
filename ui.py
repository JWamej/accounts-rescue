from customwidgets import *
from typing import Any, Literal
from customtkinter import (CTk, CTkToplevel, CTkFrame, CTkLabel, CTkEntry, CTkButton, CTkTextbox, END, WORD, CTkFont,
                           Variable, CTkImage, IntVar)
from tkinter.ttk import Treeview as TtkTreeview
from tkinter import filedialog, messagebox, Misc
import os
import sys

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


glob_show_keyboard = False


class MainWindow:
    def __init__(self, master: CTk):
        self.root = master

        # This might cause issues when switching between windows, but if this bind is applied to the frame, it at first
        # sets focus on the entry, and after second input calls right method
        self.root.bind('<Tab>', lambda event: self.set_focus_by_index())
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
        self.key_entry.bind('<Return>', self.confirm_init)

        self.hide_key_checkbox = CensorCheckbox(master=self.main_frame, entry=self.key_entry, str_var=hide_character)

        self.info_button = Button(master=self.main_frame,
                                  text='?',
                                  width=30,
                                  height=5,
                                  command=self.info_init)
        self.info_button.bind('<Return>', self.info_init)
        self.info_button.bind('<FocusIn>', lambda event: self.info_button.configure(fg_color=DEFAULT_BUTTON_HOVER_FG))
        self.info_button.bind('<FocusOut>', lambda event: self.info_button.configure(fg_color=DEFAULT_BUTTON_FG))

        self.settings_button = Button(master=self.main_frame,
                                      text='cfg',
                                      width=30,
                                      height=5,
                                      command=self.settings_init)
        self.settings_button.bind('<Return>', self.settings_init)
        self.settings_button.bind('<FocusIn>', lambda event: self.settings_button.configure(fg_color=DEFAULT_BUTTON_HOVER_FG))
        self.settings_button.bind('<FocusOut>', lambda event: self.settings_button.configure(fg_color=DEFAULT_BUTTON_FG))

        self.first_use_button = Button(master=self.main_frame,
                                text='First use',
                                command=self.first_use_init)
        self.first_use_button.bind('<Return>', self.first_use_init)
        self.first_use_button.bind('<FocusIn>', lambda event: self.first_use_button.configure(fg_color=DEFAULT_BUTTON_HOVER_FG))
        self.first_use_button.bind('<FocusOut>', lambda event: self.first_use_button.configure(fg_color=DEFAULT_BUTTON_FG))

        self.confirm_button = Button(master=self.main_frame,
                                     text='Confirm',
                                     command=self.confirm_init)
        self.confirm_button.bind('<Return>', self.confirm_init)
        self.confirm_button.bind('<FocusIn>', lambda event: self.confirm_button.configure(fg_color=DEFAULT_BUTTON_HOVER_FG))
        self.confirm_button.bind('<FocusOut>', lambda event: self.confirm_button.configure(fg_color=DEFAULT_BUTTON_FG))

        self.widget_dict = {1 : self.key_entry,
                            2 : self.confirm_button,
                            3 : self.first_use_button,
                            4 : self.info_button,
                            5 : self.settings_button}
        self.focus_index = IntVar(value=1)

    def set_focus_by_index(self, *args):
        index = self.focus_index.get()
        widget_to_focus_in = self.widget_dict.get(index)
        widget_to_focus_in.focus_set()

        if index == len(self.widget_dict):
            self.focus_index.set(1)
        else:
            self.focus_index.set(index + 1)

        return "break"  # stops tkinter from calling default behaviour after '<Tab>' event

    def info_init(self, *args):
        raise NotImplementedError

    def settings_init(self, *args):
        raise NotImplementedError

    def first_use_init(self, *args):
        raise NotImplementedError

    def confirm_init(self, *args):
        raise NotImplementedError

    def draw(self):
        self.main_frame.pack()
        self.title_label.grid(row=0, column=0, columnspan=3, padx=5, pady=(5, 0))
        self.key_entry.grid(row=1, column=0, columnspan=2, padx=5, pady=(5, 0))
        self.hide_key_checkbox.grid(row=1, column=2, padx=5, pady=(5, 0))
        self.info_button.grid(row=0, column=0, sticky='nw', padx=5, pady=(5, 0))
        self.settings_button.grid(row=0, column=0, sticky='nw', padx=(40, 5), pady=(5, 0))
        self.first_use_button.grid(row=2, column=0, columnspan=3, padx=5, pady=(5, 5), sticky='w')
        self.confirm_button.grid(row=2, column=0, columnspan=3, padx=5, pady=(5, 5), sticky='e')

    def exit(self, *args):
        self.main_frame.destroy()



class InfoWindow:
    def __init__(self):
        raise NotImplementedError


class SettingsWindow:
    def __init__(self):
        raise NotImplementedError


class FirstUseWindow:
    def __init__(self):
        raise NotImplementedError


class DisplayWindow:
    def __init__(self):
        raise NotImplementedError
