from tkinter import filedialog, messagebox
import customtkinter
import os
import sys
from crypto import encrypt_str, decrypt_bytes
from main_window import MainWindow
from customtkinter import (CTkEntry, CTk, CTkButton, END, CTkTextbox, CTkLabel, CTkToplevel, BooleanVar, IntVar,
                           CTkCheckBox)


ROOT_BG = 'black'
WIDGET_FG = '#4a0064'
BUTTON_FG = '#650089'
TEXTCOLOR = '#dbdbdc'
WIDGET_BORDER_COLOR = '#818181'
WIDGET_BORDERWIDTH = 2
FONT_NORMAL = ('Arial', 12)
FONT_BIG = ('Arial', 18)


if __name__ == '__main__':
    root = CTk()
    root.title('Get Passwords')
    root.configure(fg_color=ROOT_BG)

    main_window = MainWindow(master=root)
    main_window.draw()

    root.mainloop()






