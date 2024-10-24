from tkinter import filedialog, messagebox
import customtkinter
import os
import sys
from crypto import encrypt_str
from censor_checkbox import CensorCheckbox
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


class FirstUseWindow:
    def __init__(self, master: CTk):
        self.root = master

        self.key = os.urandom(32)
        print(self.key)
        self.iv = os.urandom(16)
        print(self.iv)

        self.title_label = CTkLabel(master=self.root, text='Create a source file', font=FONT_BIG, text_color=TEXTCOLOR)
        self.key_entry = CTkEntry(master=self.root, width=300, font=FONT_NORMAL, placeholder_text='Encryption Key',
                                  fg_color=WIDGET_FG, text_color=TEXTCOLOR, border_color=WIDGET_BORDER_COLOR,
                                  border_width=WIDGET_BORDERWIDTH)
        self.key_entry.insert(0, str(self.key)[2:-1])
        self.key_entry.configure(state='disabled')
        self.copy_button_key = CTkButton(master=self.root, text='Copy key', text_color=TEXTCOLOR, fg_color=BUTTON_FG,
                                         font=FONT_NORMAL, border_width=WIDGET_BORDERWIDTH,
                                         border_color=WIDGET_BORDER_COLOR,
                                         command=lambda: (copy_clipboard(entry=self.key_entry)))

        self.iv_entry = CTkEntry(master=self.root, width=300, font=FONT_NORMAL,
                                 placeholder_text='Initialization Vector', fg_color=WIDGET_FG, text_color=TEXTCOLOR,
                                 border_color=WIDGET_BORDER_COLOR, border_width=WIDGET_BORDERWIDTH)
        self.iv_entry.insert(0, str(self.iv)[2:-1])
        self.iv_entry.configure(state='disabled')
        self.copy_button_iv = CTkButton(master=self.root, text='Copy', text_color=TEXTCOLOR, fg_color=BUTTON_FG,
                                        font=FONT_NORMAL, border_width=WIDGET_BORDERWIDTH,
                                        border_color=WIDGET_BORDER_COLOR,
                                        command=lambda: (copy_clipboard(entry=self.iv_entry)))

        self.file_entry = CTkEntry(master=self.root, width=300, font=FONT_NORMAL, placeholder_text='Source File',
                                   fg_color=WIDGET_FG, text_color=TEXTCOLOR, border_color=WIDGET_BORDER_COLOR,
                                   border_width=WIDGET_BORDERWIDTH, state='disabled')

        self.browse_dirs_button = CTkButton(master=self.root, font=FONT_NORMAL,
                                            text='Select the directory',
                                            fg_color=WIDGET_FG, text_color=TEXTCOLOR, border_color=WIDGET_BORDER_COLOR,
                                            border_width=WIDGET_BORDERWIDTH, command=self.browse_dirs)
        self.confirm_button = CTkButton(master=self.root, text='Confirm', font=FONT_NORMAL, text_color=TEXTCOLOR,
                                        fg_color=BUTTON_FG, border_color=WIDGET_BORDER_COLOR,
                                        border_width=WIDGET_BORDERWIDTH, command=self.confirm)

    def confirm(self):
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


            with open(fr'{self.file_entry.get()}\src.txt', 'xb') as file:
                file.write(test_data + b'<SEPARATOR>')
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
        self.title_label.destroy()
        self.key_entry.destroy()
        self.copy_button_key.destroy()
        self.iv_entry.destroy()
        self.copy_button_iv.destroy()
        self.file_entry.destroy()
        self.browse_dirs_button.destroy()
        self.confirm_button.destroy()

