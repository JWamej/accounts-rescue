from tkinter import filedialog, messagebox
import customtkinter
from customtkinter import (CTkEntry, CTk, CTkButton, END, CTkTextbox, CTkLabel, CTkToplevel, BooleanVar, IntVar,
                           CTkCheckBox)
import os
import sys
from crypto import encrypt_str, decrypt_bytes


ROOT_BG = 'black'
WIDGET_FG = '#4a0064'
BUTTON_FG = '#650089'
TEXTCOLOR = '#dbdbdc'
WIDGET_BORDER_COLOR = '#818181'
WIDGET_BORDERWIDTH = 2
FONT_NORMAL = ('Arial', 12)
FONT_BIG = ('Arial', 18)


class AddEmail:
    def __init__(self, master: CTk, file_path: str, key: bytes, iv: bytes):
        self.root = CTkToplevel(master, fg_color=ROOT_BG)

        self.censor_password = IntVar(value=1)
        self.file_path = file_path
        self.key = key
        self.iv = iv

        self.title_label = CTkLabel(master=self.root, text='Add Email', font=FONT_BIG)
        self.email_entry = CTkEntry(master=self.root, width=100, font=FONT_NORMAL, border_color=WIDGET_BORDER_COLOR,
                                    border_width=WIDGET_BORDERWIDTH, state='disabled', fg_color=WIDGET_FG,
                                    placeholder_text='E-Mail')
        self.password_entry = CTkEntry(master=self.root, width=100, font=FONT_NORMAL, border_color=WIDGET_BORDER_COLOR,
                                       border_width=WIDGET_BORDERWIDTH, state='disabled', fg_color=WIDGET_FG,
                                       show=['', '*'][self.censor_password.get()], placeholder_text='Password')
        self.toggle_censor_checkbox = CTkCheckBox(master=self.root, text='Hide', compound='right', font=FONT_NORMAL,
                                                  variable=self.censor_password, onvalue=1, offvalue=0)
        self.confirm_button = CTkButton(master=self.root, text='Confirm', fg_color=BUTTON_FG, font=FONT_NORMAL,
                                        border_width=WIDGET_BORDERWIDTH, border_color=WIDGET_BORDER_COLOR,
                                        command=self.confirm, width=70, height=5)

    def draw(self):
        self.title_label.grid(row=0, column=0, columnspan=2, padx=10, pady=(5,0))
        self.email_entry.grid(row=1, column=0, padx=10, pady=(5,0))
        self.password_entry.grid(row=2, column=0, padx=10, pady=(5,0))
        self.toggle_censor_checkbox.grid(row=2, column=1, padx=10, pady=(5,0))
        self.confirm_button.grid(row=3, column=0, columnspan=2, padx=10, pady=5)

    def destroy(self):
        self.title_label.destroy()
        self.email_entry.destroy()
        self.password_entry.destroy()
        self.toggle_censor_checkbox.destroy()
        self.confirm_button.destroy()

    def confirm(self):
        email_plaintext: str = self.email_entry.get()
        password_plaintext: str = self.password_entry.get()

        if ('<SEPARATOR>' in email_plaintext) or ('<SEPARATOR>' in password_plaintext):
            messagebox.showerror('TextError', 'The phrase "<SEPARATOR>" cannot be used.')
            return

        data_encrypted: bytes = encrypt_str(f'{email_plaintext}<SEPARATOR>{password_plaintext}\n',
                                            self.key, self.iv)

        with open(self.file_path, 'ab') as file:
            file.write(data_encrypted)

        messagebox.showinfo('E-Mail Added', 'E-Mail added successfully.')

if __name__ == '__main__':
    root = CTk()
    root.configure(bg=ROOT_BG)
    root.title('test')

    window = AddEmail()