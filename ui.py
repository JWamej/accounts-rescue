from customwidgets import *
from typing import Any, Literal
from customtkinter import (CTk, CTkToplevel, CTkFrame, CTkLabel, CTkEntry, CTkButton, CTkTextbox, END, WORD, CTkFont,
                           Variable, CTkImage)
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
        self.title_label = Label(master=self.root,
                                 text='Welcome',
                                 font=FONT_BIG)

        self.key_entry = Entry(master=self.root,
                               placeholder_text='Enter key',
                               width=350)

        self.info_button = Button(master=self.root,
                                  text='?',
                                  width=30,
                                  height=5,
                                  command=self.info_init)

        self.settings_button = Button(master=self.root,
                                      text='cfg',
                                      width=30,
                                      height=5,
                                      command=self.settings_init)

        self.first_use = Button(master=self.root,
                                text='First use',
                                command=self.first_use_init)

        self.confirm_button = Button(master=self.root,
                                     text='Confirm',
                                     command=self.confirm_init)

    def info_init(self):
        raise NotImplementedError

    def settings_init(self):
        raise NotImplementedError

    def first_use_init(self):
        raise NotImplementedError

    def confirm_init(self):
        raise NotImplementedError

    def draw(self):
        self.title_label.grid(row=0, column=0, columnspan=2, padx=5, pady=(5, 0))
        self.key_entry.grid(row=1, column=0, columnspan=2, padx=5, pady=(5, 0))
        self.info_button.grid(row=0, column=0, sticky='nw', padx=5, pady=(5, 0))
        self.settings_button.grid(row=0, column=0, sticky='nw', padx=(40, 5), pady=(5, 0))
        self.first_use.grid(row=2, column=0, padx=5, pady=(5, 5), sticky='w')
        self.confirm_button.grid(row=2, column=1, padx=5, pady=(5, 5), sticky='e')

    def exit(self):
        self.root.destroy()
        self.title_label.destroy()
        self.key_entry.destroy()
        self.info_button.destroy()
        self.settings_button.destroy()
        self.first_use.destroy()
        self.confirm_button.destroy()


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
