from customwidgets import *
from typing import Any, Literal
from customtkinter import (CTk, CTkToplevel, CTkFrame, CTkLabel, CTkEntry, CTkButton, CTkTextbox, END, WORD, CTkFont,
                           Variable, CTkImage)
from tkinter.ttk import Treeview as TtkTreeview
from tkinter import filedialog, messagebox, Misc
import os
import sys


class MainWindow:
    def __init__(self, master: CTk):
        self.root = master
        self.key_entry = Entry()