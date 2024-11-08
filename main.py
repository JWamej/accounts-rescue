from customtkinter import CTk, CTkFrame, CTkLabel, CTkEntry, CTkButton, END, WORD
from tkinter.ttk import Treeview
from tkinter import filedialog, messagebox
import os
import sys
from customwidgets import Window
from ui import *


if __name__ == '__main__':
    root = Window(min_size=(200, 100))
    root.resizable(False, False)

    MainWindow(master=root).draw()

    root.mainloop()