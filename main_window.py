from tkinter import filedialog, messagebox
import customtkinter
import os
import sys
from crypto import encrypt_str, decrypt_bytes
from first_use_window import FirstUseWindow
from display_window import DisplayWindow
from censor_checkbox import CensorCheckbox
from customtkinter import (CTkEntry, CTk, CTkButton, END, CTkTextbox, CTkLabel, CTkToplevel, BooleanVar, IntVar,
                           CTkCheckBox, StringVar)
from info_window import InfoWindow


ROOT_BG = 'black'
WIDGET_FG = '#4a0064'
BUTTON_FG = '#650089'
TEXTCOLOR = '#ffffff'
WIDGET_BORDER_COLOR = '#818181'
WIDGET_BORDERWIDTH = 1
FONT_NORMAL = ('Arial', 12)
FONT_BIG = ('Arial', 18)


class MainWindow:
    def __init__(self, master: CTk):
        self.root = master

        self.censor_key = StringVar(value='*')
        self.censor_iv = StringVar(value='*')

        self.title_label = CTkLabel(master=self.root, text='Welcome', font=FONT_BIG, text_color=TEXTCOLOR)
        self.key_entry = CTkEntry(master=self.root, width=300, font=FONT_NORMAL, placeholder_text='Encryption Key',
                                  fg_color=WIDGET_FG, text_color=TEXTCOLOR, border_color=WIDGET_BORDER_COLOR,
                                  border_width=WIDGET_BORDERWIDTH, show='*')
        self.iv_entry = CTkEntry(master=self.root, width=300, font=FONT_NORMAL, show='*',
                                 placeholder_text='Initialization Vector', fg_color=WIDGET_FG, text_color=TEXTCOLOR,
                                 border_color=WIDGET_BORDER_COLOR, border_width=WIDGET_BORDERWIDTH)
        self.file_entry = CTkEntry(master=self.root, width=300, font=FONT_NORMAL, placeholder_text='Source File',
                                   fg_color=WIDGET_FG, text_color=TEXTCOLOR, border_color=WIDGET_BORDER_COLOR,
                                   border_width=WIDGET_BORDERWIDTH, state='normal')

        # I need to initially set state='normal', because with state being 'disabled' from the beginning wouldn't allow
        # the placeholder text to appear
        self.file_entry.configure(state='disabled')
        self.file_entry.bind('<Button-1>', self.browse_files)
        self.browse_files_button = CTkButton(master=self.root, width=100, font=FONT_NORMAL,
                                             text='Select the File', fg_color=WIDGET_FG,
                                             text_color=TEXTCOLOR, border_color=WIDGET_BORDER_COLOR,
                                             border_width=WIDGET_BORDERWIDTH, command=self.browse_files)
        self.toggle_censor_key = CensorCheckbox(master=self.root, entry=self.key_entry, str_var=self.censor_key,
                                                font=FONT_NORMAL, text_color=TEXTCOLOR).get()
        self.toggle_censor_iv = CensorCheckbox(master=self.root, entry=self.iv_entry, str_var=self.censor_iv,
                                               font=FONT_NORMAL, text_color=TEXTCOLOR).get()
        self.confirm_button = CTkButton(master=self.root, text='Confirm', font=FONT_NORMAL, text_color=TEXTCOLOR,
                                        fg_color=BUTTON_FG, border_color=WIDGET_BORDER_COLOR,
                                        border_width=WIDGET_BORDERWIDTH, command=self.confirm)
        self.first_use_button = CTkButton(master=self.root, text='First Use', font=FONT_NORMAL, text_color=TEXTCOLOR,
                                          fg_color=BUTTON_FG, border_color=WIDGET_BORDER_COLOR,
                                          border_width=WIDGET_BORDERWIDTH, command=self.first_use)
        self.info_button = CTkButton(master=self.root, text='?', width=30, height=5, font=FONT_NORMAL,
                                     text_color=TEXTCOLOR, fg_color=BUTTON_FG, command=self.info)

    def browse_files(self, *args):
        file = filedialog.askopenfilename(title='Select the Source File')
        self.file_entry.configure(state='normal')
        self.file_entry.insert(0, file)
        self.file_entry.configure(state='disabled')

    def confirm(self):
        key = self.key_entry.get()
        iv = self.iv_entry.get()
        file = self.file_entry.get()

        if key == '':
            messagebox.showerror('Error', 'Invalid Key')
            return
        if iv == '':
            messagebox.showerror('Error', 'Invalid IV')
            return
        if file == '':
            messagebox.showerror('Error', 'Invalid File Path')
            return

        # mostly to combat the space/endline caused by pasting the key/iv
        key = key.removesuffix(' ').removesuffix('\n')
        iv = iv.removesuffix(' ').removesuffix('\n')

        key = bytes(key, "latin1").decode("unicode_escape").encode("latin1")
        iv = bytes(iv, "latin1").decode("unicode_escape").encode("latin1")

        # this ast.literal_eval looks weird, but it basically just converts the str into bytes
        # without fucking everything up :)
        display = DisplayWindow(self.root, key, iv, file)
        display.validate_key_iv()
        self.destroy()
        display.collect_data()
        display.draw()
        display.write_data_on_textbox()
        display.update_text()

    def first_use(self):
        first_use_window = FirstUseWindow(master=self.root)
        first_use_window.draw()

    def info(self):
        window_info = InfoWindow(master=self.root)
        window_info.draw()

    def draw(self):
        self.info_button.grid(row=0, column=0, columnspan=2, pady=(3, 0), padx=(0, 5), sticky='ne')
        self.title_label.grid(row=0, column=0, columnspan=2, pady=(5, 0), padx=10)
        self.key_entry.grid(row=1, column=0, pady=(5, 0), padx=10)
        self.toggle_censor_key.grid(row=1, column=1, pady=(5, 0), padx=10)
        self.iv_entry.grid(row=2, column=0, pady=(5, 0), padx=10)
        self.toggle_censor_iv.grid(row=2, column=1, pady=(5, 0), padx=10)
        self.file_entry.grid(row=3, column=0, pady=(5, 0), padx=10)
        self.browse_files_button.grid(row=3, column=1, pady=(5, 0), padx=10)
        self.confirm_button.grid(row=4, column=0, columnspan=2, pady=(10, 5), padx=10, sticky='w')
        self.first_use_button.grid(row=4, column=0, columnspan=2, pady=(10, 5), padx=10, sticky='e')

    def destroy(self):
        self.title_label.destroy()
        self.key_entry.destroy()
        self.toggle_censor_key.destroy()
        self.iv_entry.destroy()
        self.toggle_censor_iv.destroy()
        self.file_entry.destroy()
        self.browse_files_button.destroy()
        self.confirm_button.destroy()
        self.first_use_button.destroy()


if __name__ == '__main__':
    root = CTk()
    root.title('Test')
    root.configure(fg_color=ROOT_BG)

    MainWindow(master=root).draw()

    root.mainloop()
