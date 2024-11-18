from customtkinter import CTk, CTkFrame, CTkLabel, CTkEntry, CTkButton, END, WORD
from tkinter.ttk import Treeview
from tkinter import filedialog, messagebox
import os
import sys
from customwidgets import Window
from ui import *


if __name__ == '__main__':
    root_size = (650, 700)
    root = Window(min_size=root_size, fg_color='black')
    root.resizable(False, False)
    root.attributes('-alpha', 0.0)
    root.after(0, lambda: root.attributes('-alpha', 1.0))  # TODO change time to 1500

    placeholder = CTkFrame(master=root, width=root_size[0], height=root_size[1], fg_color='black').place(x=0, y=0)

    main_window = MainWindow(master=root, info_window=None, display_window=None, first_use_window=None)

    info_window = InfoWindow()
    first_use_window = FirstUseWindow(master=root, main_window=main_window)
    display_window = DisplayWindow()

    # This seems completely illogical (and most probably is), but this is the only solution I could have found to
    # basically create the equivalence of a circular import. This voodoo works only because the MainWindow.__init__
    # saves these objects as a variable, but doesn't use them until some user input. Basically it works unless the
    # user finds a way to interact with widgets before main_window.update_objects() is called,
    # which *should* be impossible
    main_window.update_objects(new_info_window_obj=info_window, new_first_use_obj=first_use_window,
                               new_display_window_obj=display_window)


    root.mainloop()
