from tkinter import filedialog, messagebox
import customtkinter
from customtkinter import (CTkEntry, CTk, CTkButton, END, CTkTextbox, CTkLabel, CTkToplevel, BooleanVar, IntVar,
                           CTkCheckBox, StringVar, CTkOptionMenu)
import os
import sys
from crypto import encrypt_str, decrypt_bytes
from censor_checkbox import CensorCheckbox


ROOT_BG = 'black'
WIDGET_FG = '#4a0064'
BUTTON_FG = '#650089'
TEXTCOLOR = '#ffffff'
WIDGET_BORDER_COLOR = '#818181'
WIDGET_BORDERWIDTH = 1
FONT_NORMAL = ('Arial', 12)
FONT_BIG = ('Arial', 18)


class DeleteEmail:
    def __init__(self, master: CTk, key: bytes, iv: bytes, file: str):
        self.root = CTkToplevel(master)
        self.root.configure(fg_color=ROOT_BG)
        self.root.title('Delete E-Mail')

        self.key = key
        self.iv = iv
        self.file = file

        self.title_label = CTkLabel(master=self.root, text='Delete E-Mail', fg_color=WIDGET_FG, font=FONT_BIG)
        self.email_delete_option = CTkOptionMenu(master=self.root, fg_color=BUTTON_FG, font=FONT_NORMAL,
                                                 values=self.get_emails())
        self.delete_button = CTkButton(master=self.root, text='Delete', fg_color=BUTTON_FG,
                                       border_color=WIDGET_BORDER_COLOR, border_width=WIDGET_BORDERWIDTH,
                                       command=self.delete_email)
        self.exit_button = CTkButton(master=self.root, text='Exit', fg_color=BUTTON_FG,
                                     border_color=WIDGET_BORDER_COLOR, border_width=WIDGET_BORDERWIDTH,
                                     command=self.destroy)

    def get_emails(self) -> list[str]:
        with open(self.file, 'rb') as file:
            data_encrypted: list = file.read().split(b'<SEPARATOR>')

        # gets rid of the sample and other useless things
        data_encrypted.pop(0)

        if data_encrypted[-1] == b'':
            data_encrypted.pop(-1)

        accounts = []
        for account in data_encrypted:
            email, password = decrypt_bytes(account, key=self.key, iv=self.iv).split('<SEPARATOR>')
            accounts.append(str(email))
        return accounts

    def get_all_raw_data(self) -> list[bytes]:
        with open(self.file, 'rb') as file:
            data_encrypted: list = file.read().split(b'<SEPARATOR>')

        return data_encrypted

    def delete_email(self):
        email_to_pop = self.email_delete_option.get()
        index_to_pop = self.get_emails().index(email_to_pop) + 1

        confirmation = messagebox.askyesno('Confirmation', f'Are you sure you want to'
                                                           f' delete {email_to_pop}?\nThis action is irreversible.')
        if not confirmation:
            return

        all_accounts = self.get_all_raw_data()
        all_accounts.pop(index_to_pop)

        # the line under is omitted to keep the b'' as the last part of the list, so in the end the file
        # ends with b'<SEPARATOR>'

        # all_accounts.pop(-1)



        with open(self.file, 'wb') as file:
            file.write(b'<SEPARATOR>'.join(all_accounts))

    def draw(self):
        self.title_label.grid(row=0, column=0, columnspan=2, pady=(5, 0), padx=10)
        self.email_delete_option.grid(row=1, column=0, columnspan=2, pady=(10, 0), padx=10)
        self.delete_button.grid(row=2, column=0, pady=10, padx=10)
        self.exit_button.grid(row=2, column=1, pady=10, padx=10)
        self.root.grab_set()
        self.root.focus_set()

    def destroy(self):
        self.root.destroy()









