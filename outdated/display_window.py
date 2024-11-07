from tkinter import filedialog, messagebox
import customtkinter
import os
import sys
from crypto import encrypt_str, decrypt_bytes, CipherError
from first_use_window import FirstUseWindow
from censor_checkbox import CensorCheckbox
from add_email import AddEmail
from delete_email import DeleteEmail
from customtkinter import (CTkEntry, CTk, CTkButton, END, WORD, CTkTextbox, CTkLabel, CTkToplevel, BooleanVar, IntVar,
                           CTkCheckBox, StringVar)


ROOT_BG = 'black'
WIDGET_FG = '#4a0064'
BUTTON_FG = '#650089'
TEXTCOLOR = '#ffffff'
WIDGET_BORDER_COLOR = '#818181'
WIDGET_BORDERWIDTH = 1
FONT_NORMAL = ('Arial', 12)
FONT_BIG = ('Arial', 18)


class DisplayWindow:
    def __init__(self, master: CTk, key: bytes, iv: bytes, file: str):
        self.root = master
        self.root.title('Display')
        self.key = key
        self.iv = iv
        self.src_file = file
        self.decrypted_data: list[tuple[str, str]] = []

        self.title_label = CTkLabel(master=self.root, text='E-Mails and Passwords:', text_color=TEXTCOLOR,
                                    font=FONT_BIG)
        self.inputs_textbox = CTkTextbox(master=self.root, text_color=TEXTCOLOR, fg_color=WIDGET_FG, state='disabled',
                                         font=FONT_NORMAL, border_color=WIDGET_BORDER_COLOR, wrap=WORD,
                                         border_width=WIDGET_BORDERWIDTH, width=800, height=400)
        self.add_email_button = CTkButton(master=self.root, text_color=TEXTCOLOR, fg_color=BUTTON_FG,
                                          text='Add E-Mail', command=self.email_add,
                                          border_color=WIDGET_BORDER_COLOR, border_width=WIDGET_BORDERWIDTH)
        self.delete_email_button = CTkButton(master=self.root, text_color=TEXTCOLOR, fg_color=BUTTON_FG,
                                             text='Delete E-Mail', command=self.email_delete,
                                             border_color=WIDGET_BORDER_COLOR, border_width=WIDGET_BORDERWIDTH)
        self.exit_button = CTkButton(master=self.root, text_color=TEXTCOLOR, fg_color=BUTTON_FG,
                                     text='Exit', command=self.destroy, border_width=WIDGET_BORDERWIDTH,
                                     border_color=WIDGET_BORDER_COLOR)

    def validate_key_iv(self):
        try:
            with open(self.src_file, 'rb') as file:
                data_list_encrypted = file.read().split(b'<SEPARATOR>')

            sample = data_list_encrypted[0]

            decrypt_bytes(sample, self.key, self.iv)
        except ValueError as e:
            messagebox.showerror('Error', f'Error code: DW-KEYLEN\n{e}')
        except CipherError as e:
            messagebox.showerror('Error', f'Error code: DW-CE\n{e}')

    def collect_data(self):
        # otherwise the self.update_textbox() infinitely appends the list
        self.decrypted_data = []

        with open(self.src_file, 'rb') as file:
            data_list_encrypted = file.read().split(b'<SEPARATOR>')

        accounts_decrypted = []

        # Gets rid of the sample
        data_list_encrypted.pop(0)

        # otherwise there is a padding error
        if data_list_encrypted[-1] == b'':
            data_list_encrypted.pop(-1)

        for account in data_list_encrypted:
            accounts_decrypted.append(decrypt_bytes(account, self.key, self.iv))

        for account in accounts_decrypted:
            email, password = account.split('<SEPARATOR>')
            self.decrypted_data.append((str(email), str(password)))

    def write_data_on_textbox(self):
        self.inputs_textbox.configure(state='normal')
        for account in self.decrypted_data:
            self.inputs_textbox.insert(END, f'{account[0]}\n{account[1]}\n\n')
        self.inputs_textbox.configure(state='disabled')

    def update_text(self):
        collected_data_snapshot = self.decrypted_data
        self.collect_data()
        if not collected_data_snapshot == self.decrypted_data:
            self.inputs_textbox.configure(state='normal')
            self.inputs_textbox.delete(0.0, END)
            self.inputs_textbox.configure(state='disabled')
            self.write_data_on_textbox()
        self.root.after(250, self.update_text)

    def email_add(self):
        email_window = AddEmail(master=self.root, key=self.key, iv=self.iv, file_path=self.src_file)
        email_window.draw()

    def email_delete(self):
        email_window = DeleteEmail(master=self.root, key=self.key, iv=self.iv, file=self.src_file)
        email_window.draw()

    def destroy(self):
        self.root.destroy()

    def draw(self):
        self.title_label.grid(row=0, column=0, columnspan=3, pady=(5, 0), padx=5)
        self.inputs_textbox.grid(row=1, column=0, columnspan=3, pady=(5, 0), padx=5)
        self.add_email_button.grid(row=2, column=0, pady=5, padx=10)
        self.exit_button.grid(row=2, column=1, pady=5, padx=10)
        self.delete_email_button.grid(row=2, column=2, pady=5, padx=10)

