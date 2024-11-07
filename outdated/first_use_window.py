from tkinter import filedialog, messagebox
import customtkinter
import os
import sys
from crypto import encrypt_str
from random import randint
import pyperclip
from customtkinter import (CTkEntry, CTk, CTkButton, END, CTkTextbox, CTkLabel, CTkToplevel, BooleanVar, IntVar,
                           StringVar, CTkCheckBox)


ROOT_BG = 'black'
WIDGET_FG = '#4a0064'
BUTTON_FG = '#650089'
TEXTCOLOR = '#ffffff'
WIDGET_BORDER_COLOR = '#818181'
WIDGET_BORDERWIDTH = 1
FONT_NORMAL = ('Arial', 12)
FONT_BIG = ('Arial', 18)


def copy_clipboard(entry: CTkEntry):
    pyperclip.copy(entry.get())


# I kind of dislike this implementation, but around ~45% of the results of os.urandom() result in some kind of error
# (for example ' and " basically sql-injecting themselves or '\n' causing every singe str -> bytes conversion method to
# stop working [needed in main_window.py])
def generate_key() -> bytes:
    while True:
        key = os.urandom(32)

        if (b'"' in key) or (b"'" in key) or (b'\n' in key) or (b' ' in key):
            continue
        return key


def generate_iv() -> bytes:
    while True:
        iv = os.urandom(16)

        if (b'"' in iv) or (b"'" in iv) or (b'\n' in iv) or (b' ' in iv):
            continue
        return iv


class FirstUseWindow:
    def __init__(self, master: CTk):
        self.root = CTkToplevel(master=master)
        self.root.configure(fg_color=ROOT_BG)
        self.root.title('First Use')
        self.root.grab_set()
        self.root.focus_set()

        self.key = generate_key()
        self.iv = generate_iv()

        self.title_label = CTkLabel(master=self.root, text='Create a source file', font=FONT_BIG, text_color=TEXTCOLOR)
        self.key_entry = CTkEntry(master=self.root, width=600, font=FONT_NORMAL, placeholder_text='Encryption Key',
                                  fg_color=WIDGET_FG, text_color=TEXTCOLOR, border_color=WIDGET_BORDER_COLOR,
                                  border_width=WIDGET_BORDERWIDTH)
        self.key_entry.insert(0, str(self.key)[2:-1])
        self.key_entry.configure(state='disabled')
        self.copy_button_key = CTkButton(master=self.root, text='Copy key', text_color=TEXTCOLOR, fg_color=BUTTON_FG,
                                         font=FONT_NORMAL, border_width=WIDGET_BORDERWIDTH,
                                         border_color=WIDGET_BORDER_COLOR,
                                         command=lambda: (copy_clipboard(entry=self.key_entry)))

        self.iv_entry = CTkEntry(master=self.root, width=600, font=FONT_NORMAL,
                                 placeholder_text='Initialization Vector', fg_color=WIDGET_FG, text_color=TEXTCOLOR,
                                 border_color=WIDGET_BORDER_COLOR, border_width=WIDGET_BORDERWIDTH)
        self.iv_entry.insert(0, str(self.iv)[2:-1])
        self.iv_entry.configure(state='disabled')
        self.copy_button_iv = CTkButton(master=self.root, text='Copy vector', text_color=TEXTCOLOR, fg_color=BUTTON_FG,
                                        font=FONT_NORMAL, border_width=WIDGET_BORDERWIDTH,
                                        border_color=WIDGET_BORDER_COLOR,
                                        command=lambda: (copy_clipboard(entry=self.iv_entry)))

        self.file_entry = CTkEntry(master=self.root, width=600, font=FONT_NORMAL, placeholder_text='Source File',
                                   fg_color=WIDGET_FG, text_color=TEXTCOLOR, border_color=WIDGET_BORDER_COLOR,
                                   border_width=WIDGET_BORDERWIDTH, state='disabled')

        self.browse_dirs_button = CTkButton(master=self.root, font=FONT_NORMAL,
                                            text='Select directory',
                                            fg_color=BUTTON_FG, text_color=TEXTCOLOR, border_color=WIDGET_BORDER_COLOR,
                                            border_width=WIDGET_BORDERWIDTH, command=self.browse_dirs)
        self.confirm_button = CTkButton(master=self.root, text='Confirm', font=FONT_NORMAL, text_color=TEXTCOLOR,
                                        fg_color=BUTTON_FG, border_color=WIDGET_BORDER_COLOR,
                                        border_width=WIDGET_BORDERWIDTH, command=self.confirm)
        self.exit_button = CTkButton(master=self.root, text='Exit', font=FONT_NORMAL, text_color=TEXTCOLOR,
                                     fg_color=BUTTON_FG, border_color=WIDGET_BORDER_COLOR,
                                     border_width=WIDGET_BORDERWIDTH, command=self.destroy)

    def confirm(self):
        if self.file_entry.get() == '' or (not os.path.isdir(self.file_entry.get())):
            messagebox.showerror('Error', 'Error code: FUW-DIR\nInvalid Directory')
            return
        ask_if_ready = messagebox.askyesno('Confirmation', 'After finishing this configuration you will no'
                                                           ' longer be able to get access to the key and initialization'
                                                           ' vector, which will be necessary to later decrypt the'
                                                           ' source file.\nAre you sure you wand to end the'
                                                           ' configuration?')
        if not ask_if_ready:
            return

        try:
            test_data = encrypt_str(plain_text=str(f'{randint(a=1000000000000000000, b=10000000000000000000000)}'),
                                    key=self.key, iv=self.iv)
            if b'<SEPARATOR>' in test_data:
                messagebox.showerror('Error', 'Error code: FUW-SEPERR')


            with open(fr'{self.file_entry.get()}\src', 'xb') as file:
                file.write(test_data + b'<SEPARATOR>')
            self.root.destroy()
        except FileExistsError:
            messagebox.showerror('Error', 'Error code: FUW-FEE\n\nThere is already a source file in '
                                          'selected directory.')
        except ValueError:
            messagebox.showerror('Error', 'Error code: FUW-CRYPT-VE')

    def browse_dirs(self):
        file = filedialog.askdirectory(title='Select the Source File')
        self.file_entry.configure(state='normal')
        self.file_entry.insert(0, file)
        self.file_entry.configure(state='disabled')

    def draw(self):
        self.title_label.grid(row=0, column=0, columnspan=2, pady=(5, 0), padx=10)
        self.key_entry.grid(row=1, column=0, pady=(5, 0), padx=10)
        self.copy_button_key.grid(row=1, column=1, pady=(5, 0), padx=10)
        self.iv_entry.grid(row=2, column=0, pady=(5, 0), padx=10)
        self.copy_button_iv.grid(row=2, column=1, pady=(5, 0), padx=10)
        self.file_entry.grid(row=3, column=0, pady=(5, 0), padx=10)
        self.browse_dirs_button.grid(row=3, column=1, pady=(5, 0), padx=10)
        self.confirm_button.grid(row=4, column=0, columnspan=2, pady=(10, 5), padx=10, sticky='w')

    def destroy(self):
        self.root.destroy()
