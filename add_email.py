from tkinter import filedialog, messagebox
import customtkinter
from customtkinter import (CTkEntry, CTk, CTkButton, END, CTkTextbox, CTkLabel, CTkToplevel, BooleanVar, IntVar,
                           CTkCheckBox, StringVar)
import os
import sys
from crypto import encrypt_str, decrypt_bytes
from main_window import CensorCheckbox


ROOT_BG = 'black'
WIDGET_FG = '#4a0064'
BUTTON_FG = '#650089'
TEXTCOLOR = '#ffffff'
WIDGET_BORDER_COLOR = '#818181'
WIDGET_BORDERWIDTH = 1
FONT_NORMAL = ('Arial', 12)
FONT_BIG = ('Arial', 18)


class AddEmail:
    def __init__(self, master: CTk, file_path: str, key: bytes, iv: bytes):
        self.root = CTkToplevel(master)
        self.root.configure(fg_color=ROOT_BG)

        self.censor_password = StringVar(value='*')
        self.file_path = file_path
        self.key = key
        self.iv = iv

        self.title_label = CTkLabel(master=self.root, text='Add Email', font=FONT_BIG, text_color=TEXTCOLOR)
        self.email_entry = CTkEntry(master=self.root, width=300, font=FONT_NORMAL, border_color=WIDGET_BORDER_COLOR,
                                    border_width=WIDGET_BORDERWIDTH, fg_color=WIDGET_FG, text_color=TEXTCOLOR,
                                    placeholder_text='E-Mail')
        self.password_entry = CTkEntry(master=self.root, width=300, font=FONT_NORMAL, border_color=WIDGET_BORDER_COLOR,
                                       border_width=WIDGET_BORDERWIDTH, fg_color=WIDGET_FG, text_color=TEXTCOLOR,
                                       show='*', placeholder_text='Password')
        self.confirm_button = CTkButton(master=self.root, text='Confirm', fg_color=BUTTON_FG, font=FONT_NORMAL,
                                        border_width=WIDGET_BORDERWIDTH, border_color=WIDGET_BORDER_COLOR,
                                        command=self.confirm, width=100, height=5, text_color=TEXTCOLOR)
        self.toggle_censor_checkbox = CensorCheckbox(master=self.root, entry=self.password_entry,
                                                     str_var=self.censor_password, font=FONT_NORMAL,
                                                     text_color=TEXTCOLOR).get()

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
            messagebox.showerror('Error', 'Error code: AE-SEPPERR\n'
                                          'The phrase "<SEPARATOR>" cannot be used.')
            return

        data_encrypted: bytes = encrypt_str(f'{email_plaintext}<SEPARATOR>{password_plaintext}',
                                            self.key, self.iv)

        with open(self.file_path, 'ab') as file:
            file.write(data_encrypted + b'<SEPARATOR>')

        messagebox.showinfo('E-Mail Added', 'E-Mail added successfully.')


if __name__ == '__main__':
    root = CTk()
    root.configure(fg_color=ROOT_BG)
    root.title('test')

    key = b'\xb8\x86\xb9\xf0\x07\xb2\xcc\xa16o\xce\xcc\x15\xbbO@\x18\x95}\xfb\xf4x\x1fq,\xc5\x8b\x8bMy\x13b'
    iv = b'\xf8\x83}\xfe\xd0\xc5R\xdc)\xb0\xe6\x1d5\x12\xd5\xbc'

    window = AddEmail(master=root, file_path=fr'{os.path.expanduser("~")}\Desktop\src.txt', key=key, iv=iv)
    window.draw()

    root.mainloop()
    
