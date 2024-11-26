from customwidgets import *
import os
import sys
from tkinter import filedialog, messagebox
from typing import Union

import pyperclip
from customtkinter import (CTk, CTkFrame, CTkEntry, CTkButton, CTkTextbox, END, IntVar)

from crypto import *
from customwidgets import *

DEFAULT_ROOT_FG = 'black'
DEFAULT_FRAME_FG = '#1c0016'
DEFAULT_WIDGET_FG = '#4a0064'
DEFAULT_BUTTON_FG = '#650089'
DEFAULT_BUTTON_HOVER_FG = '#46004c'
DEFAULT_TEXTCOLOR = '#ffffff'
DEFAULT_TEXTCOLOR_DISABLED = '#818181'
DEFAULT_TEXTCOLOR_PLACEHOLDER = DEFAULT_TEXTCOLOR_DISABLED
DEFAULT_BORDER_COLOR = '#4c4c4c'
DEFAULT_BORDERWIDTH = 1
FONT_NORMAL = ('Arial', 12)
FONT_BIG = ('Arial', 18)


# Notes
# 1. The keyboard is a part of MainWindow, but it is always displayed even when the actual
#    main_frame is hidden. This is because making it an independent class would create issues
#    where MainWindow class needs KeyboardFrame to be generated, but KeyboardFrame also needs
#    MainWindow to be generated. I kind of made it work in main.py, but I would rather not repeat
#    that solution too often, because it is most likely bug-inducing.
#
# 2. In the DisplayWindow the variables referring to the position of an item/account on a treeview / in the list
#    have either "nr" or "index" in their names. The difference between them is that nr means the displayable
#    position of an item/account (min value = 1), whereas index means the position of an item/account
#    in the list (min value = 0). This has been introduced to avoid confusion with the whole index = index - 1 debacle.


def browse_dirs(entry: CTkEntry):
    selected_dir = filedialog.askdirectory(title='Select directory')
    if selected_dir:
        entry.configure(state='normal')
        entry.delete(0, END)
        entry.insert(0, selected_dir)
        entry.configure(state='disabled')


def browse_files(entry: CTkEntry):
    selected_dir = filedialog.askopenfilename(title='Select file')
    if selected_dir:
        entry.configure(state='normal')
        entry.delete(0, END)
        entry.insert(0, selected_dir)
        entry.configure(state='disabled')


def set_focus_by_index(index_var: IntVar, widget_dict: dict, *args):
    """
    Sets the focus on the widget connected to the index in the dict.
    :param index_var:
    :param widget_dict:
    :param args:
    :return:
    """
    index = index_var.get()
    widget_to_focus_in = widget_dict.get(index)
    widget_to_focus_in.focus_set()

    if index == len(widget_dict):
        index_var.set(1)
    else:
        index_var.set(index + 1)

    return "break"  # stops tkinter from calling default behaviour after '<Tab>' event


def set_binds_buttons(button: CTkButton, command: () = None):
    button.bind('<FocusIn>', lambda event: button.configure(fg_color=DEFAULT_BUTTON_HOVER_FG))
    button.bind('<FocusOut>', lambda event: button.configure(fg_color=DEFAULT_BUTTON_FG))
    if command:
        button.bind('<Return>', lambda event: command())


def toggle_placeholder_on_textbox(textbox: Textbox, placeholder: str, event):
    if not textbox.get(0.0, 'end').removesuffix('\n') and str(event.type) == '10':  # FocusOut
        textbox.insert(0.0, placeholder)
        textbox.configure(text_color=DEFAULT_TEXTCOLOR_PLACEHOLDER)
        return
    if str(event.type) == '9' and textbox.get(0.0, 'end').removesuffix('\n') == placeholder:  # FocusIn
        textbox.delete(0.0, 'end')
        textbox.configure(text_color=DEFAULT_TEXTCOLOR)


def bind_linking_to_keyboard(keyboard_command: (), widget: CTkEntry | CTkTextbox):
    """
    Shortcut to bind the <FocusIn> event of the widget to link the widget to the keyboard.\n
    The keyboard_command variable must be set to the KeyboardFrame.change_linked_widget()
    :param keyboard_command:
    :param widget:
    :return:
    """
    widget.bind('<FocusIn>', lambda event: (keyboard_command(widget)))


class MainWindow:
    def __init__(self, master: CTk,
                 info_window: Union["InfoWindow", None],
                 display_window: Union["DisplayWindow", None],
                 setup_window: Union["SetupWindow", None]):
        self.root = master

        self.info_window_obj = info_window
        self.display_window_obj = display_window
        self.setup_obj = setup_window

        # This might cause issues when switching between windows, but if this bind is applied to the frame, it at first
        # sets focus on the entry, and after second input calls the right method
        self.root.bind('<Tab>', lambda event: set_focus_by_index(self.tab_focus_index, self.widget_dict))
        self.root.bind('<Escape>', lambda event: sys.exit())

        self.placeholder = CTkFrame(master=self.root, width=650, height=435, fg_color='black')

        self.keyboard_frame = KeyboardFrame(master=self.root,
                                            write_on=self.root)

        self.main_frame = Frame(master=self.root)

        self.title_label = Label(master=self.main_frame,
                                 text='Welcome')

        hide_character = StringVar(value='*')
        self.key_entry = Entry(master=self.main_frame,
                               placeholder_text='Enter key',
                               width=325,
                               show=hide_character.get())
        bind_linking_to_keyboard(widget=self.key_entry,
                                 keyboard_command=self.keyboard_frame.change_linked_widget)

        self.show_key_checkbox = CensorCheckbox(master=self.main_frame, entry=self.key_entry, str_var=hide_character)

        self.file_entry = Entry(master=self.main_frame,
                                placeholder_text='Select source file',
                                width=325)
        bind_linking_to_keyboard(widget=self.file_entry,
                                 keyboard_command=self.keyboard_frame.change_linked_widget)

        self.browse_files_button = Button(master=self.main_frame,
                                          text='Browse',
                                          command=lambda: browse_files(entry=self.file_entry))
        set_binds_buttons(button=self.browse_files_button, command=lambda: browse_files(entry=self.file_entry))

        self.info_button = Button(master=self.main_frame,
                                  text='?',
                                  width=30,
                                  height=5,
                                  command=self.info_init)
        set_binds_buttons(button=self.info_button, command=self.info_init)

        self.setup_button = Button(master=self.main_frame,
                                   text='Setup',
                                   command=self.setup_init)
        set_binds_buttons(button=self.setup_button, command=self.setup_init)

        self.confirm_button = Button(master=self.main_frame,
                                     text='Confirm',
                                     command=self.display_init)
        set_binds_buttons(button=self.confirm_button, command=self.display_init)

        self.widget_dict = {1: self.key_entry,
                            2: self.file_entry,
                            3: self.browse_files_button,
                            4: self.confirm_button,
                            5: self.setup_button,
                            6: self.info_button}

        self.tab_focus_index = IntVar(value=1)

        self.placeholder.place(x=0, y=0)
        self.main_frame.place(relx=0.5, rely=0.126, anchor='n')
        self.keyboard_frame.place(relx=0.5, rely=0.99, anchor='s')
        self.title_label.grid(row=0, column=0, columnspan=2, padx=5, pady=(10, 10))
        self.key_entry.grid(row=1, column=0, padx=(10, 5), pady=(5, 0))
        self.show_key_checkbox.grid(row=1, column=1, padx=5, pady=(5, 0), sticky='w')
        self.file_entry.grid(row=2, column=0, padx=(10, 5), pady=(5, 0))
        self.browse_files_button.grid(row=2, column=1, padx=(5, 10), pady=(5, 0), sticky='w')
        self.info_button.grid(row=0, column=0, sticky='nw', padx=(10, 5), pady=(10, 0))
        self.setup_button.grid(row=3, column=0, columnspan=3, padx=(10, 5), pady=(10, 10), sticky='w')
        self.confirm_button.grid(row=3, column=0, columnspan=3, padx=(5, 10), pady=(10, 10), sticky='e')

    def info_init(self, *args):
        raise NotImplementedError

    def setup_init(self):
        self.setup_obj.setup_frame.lift()
        self.main_frame.lower(self.placeholder)
        self.keyboard_frame.change_linked_widget(
            self.setup_obj.widget_dict[self.setup_obj.keyboard_current_focus.get()])
        self.root.bind('<Tab>', lambda event: set_focus_by_index(self.setup_obj.tab_focus_index,
                                                                 self.setup_obj.widget_dict))
        self.setup_obj.key_entry.delete(0, 'end')
        self.setup_obj.key_entry.insert(0, generate_key())

    def display_init(self):
        src_file = self.file_entry.get()
        user_key = pad_key(key=self.key_entry.get().encode())

        if not user_key:
            messagebox.showerror('Error', 'No key provided')
            return
        elif not src_file:
            messagebox.showerror('Error', 'No source file selected')
            return
        elif not os.path.isfile(src_file):
            messagebox.showerror('Error', 'Selected file does not exist')
            return

        elif not validate_key(src_file_path=src_file, key=user_key):
            messagebox.showerror('Error', 'Provided key does not match the '
                                          'cipher used to encrypt the file')
            return

        self.display_window_obj.verified_key = user_key
        self.display_window_obj.src_file = src_file

        self.display_window_obj.fill_tree()

        self.main_frame.lower(self.placeholder)
        # TODO: change the value in .after()
        self.display_window_obj.display_frame.lift()
        self.keyboard_frame.change_linked_widget(self.root)
        self.root.bind('<Tab>', lambda event: set_focus_by_index(self.display_window_obj.tab_focus_index_var,
                                                                 self.display_window_obj.widget_dict))
        self.root.bind('<Delete>', lambda event: self.display_window_obj.delete_selected_account_procedure())
        self.file_entry.delete(0, 'end')
        self.key_entry.delete(0, 'end')

    # look main.py for explanation
    def update_objects(self, new_setup_obj: "SetupWindow", new_info_window_obj: "InfoWindow",
                       new_display_window_obj: "DisplayWindow"):
        self.setup_obj = new_setup_obj
        self.info_window_obj = new_info_window_obj
        self.display_window_obj = new_display_window_obj


class InfoWindow:
    def __init__(self):
        pass


class SetupWindow:
    def __init__(self, master: CTk, main_window: MainWindow):
        self.root = master

        self.setup_frame = Frame(master=self.root)

        self.main_window_obj = main_window
        self.keyboard_frame = main_window.keyboard_frame
        hide_character = StringVar(value='*')

        self.title_label = Label(master=self.setup_frame,
                                 text='Setup')

        self.key_entry = Entry(master=self.setup_frame,
                               placeholder_text='Enter the key',
                               width=325,
                               show=hide_character.get())
        bind_linking_to_keyboard(widget=self.key_entry,
                                 keyboard_command=self.main_window_obj.keyboard_frame.change_linked_widget)

        self.show_key_checkbox = CensorCheckbox(master=self.setup_frame,
                                                entry=self.key_entry,
                                                str_var=hide_character)

        self.copy_key_button = Button(master=self.setup_frame,
                                      text='Copy',
                                      width=70,
                                      command=lambda: pyperclip.copy(self.key_entry.get()))
        set_binds_buttons(button=self.copy_key_button, command=lambda: pyperclip.copy(self.key_entry.get()))

        self.directory_entry = Entry(master=self.setup_frame,
                                     placeholder_text='Select directory',
                                     width=325)
        bind_linking_to_keyboard(widget=self.directory_entry,
                                 keyboard_command=self.main_window_obj.keyboard_frame.change_linked_widget)

        self.browse_dirs_button = Button(master=self.setup_frame,
                                         text='Browse',
                                         command=lambda: browse_dirs(entry=self.directory_entry))
        set_binds_buttons(button=self.browse_dirs_button, command=lambda: browse_dirs(entry=self.directory_entry))

        self.exit_button = Button(master=self.setup_frame,
                                  text='Exit',
                                  command=self.return_to_main_window)
        set_binds_buttons(button=self.exit_button, command=self.return_to_main_window)

        self.confirm_button = Button(master=self.setup_frame,
                                     text='Confirm',
                                     command=self.confirm)
        set_binds_buttons(button=self.confirm_button, command=self.confirm)

        self.widget_dict = {1: self.key_entry,
                            2: self.directory_entry,
                            3: self.copy_key_button,
                            4: self.browse_dirs_button,
                            5: self.confirm_button,
                            6: self.exit_button}

        self.tab_focus_index = IntVar(value=1)
        self.keyboard_current_focus = IntVar(value=1)

        self.setup_frame.place(relx=0.5, rely=0.126, anchor='n')
        self.setup_frame.lower(self.main_window_obj.placeholder)
        self.title_label.grid(row=0, column=0, columnspan=3, pady=(10, 10), padx=5)
        self.key_entry.grid(row=1, column=0, pady=(5, 0), padx=(10, 5))
        self.copy_key_button.grid(row=1, column=1, pady=(5, 0), padx=5)
        self.show_key_checkbox.grid(row=1, column=2, pady=(5, 0), padx=5)
        self.directory_entry.grid(row=2, column=0, pady=(5, 0), padx=(10, 5))
        self.browse_dirs_button.grid(row=2, column=1, columnspan=2, pady=(5, 0), padx=(5, 10))
        self.confirm_button.grid(row=3, column=0, columnspan=3, sticky='e', pady=(10, 10), padx=(10, 10))
        self.exit_button.grid(row=3, column=0, columnspan=3, sticky='w', pady=(10, 10), padx=(10, 5))

    def confirm(self):
        if not messagebox.askyesno('Confirmation', 'After finishing this configuration you will no'
                                                   ' longer be able to get access to the key and initialization'
                                                   ' vector, which will be necessary to later decrypt the'
                                                   ' source file.\nAre you sure you wand to end the'
                                                   ' configuration?'):
            return

        user_key = self.key_entry.get().encode()
        user_dir = self.directory_entry.get()

        if not user_key:
            messagebox.showerror('Error', "Key wasn't provided.")
            return

        elif not user_dir:
            messagebox.showerror('Error', "Directory wasn't selected.")
            return

        elif not os.path.isdir(user_dir):
            messagebox.showerror('Error', "Selected directory doesn't exist.")
            return

        if os.path.exists(fr'{user_dir}\src'):
            additional_number = 1
            while os.path.exists(fr'{user_dir}\src ({additional_number})'):
                additional_number += 1
            name_of_source_file = f'src ({additional_number})'
        else:
            name_of_source_file = 'src'

        user_key_bytes = pad_key(key=user_key)

        validation_str = 'Beautiful is better than ugly.'
        validation_str_encrypted = encrypt_str(validation_str, user_key_bytes)

        with open(fr'{user_dir}\{name_of_source_file}', 'xb') as file:
            file.write(validation_str_encrypted + b'<0>')

        self.return_to_main_window()

    def return_to_main_window(self):
        self.main_window_obj.main_frame.lift()
        self.setup_frame.lower(self.main_window_obj.placeholder)
        self.main_window_obj.keyboard_frame.change_linked_widget(self.main_window_obj.key_entry)
        self.root.bind('<Tab>', lambda event: set_focus_by_index(self.main_window_obj.tab_focus_index,
                                                                 self.main_window_obj.widget_dict))


class DisplayWindow:
    def __init__(self, master: CTk,
                 main_window: MainWindow,
                 src_file: Union[str, None],
                 verified_key: Union[bytes, None]):
        self.root = master
        self.src_file = src_file
        self.verified_key = verified_key
        self.main_window_obj = main_window

        self.display_frame = Frame(master=self.root)

        self.accounts_dict: dict[int: tuple[str, str, str, str]] = {}

        self.account_treeview = Treeview(master=self.display_frame,
                                         columns=('Nr', 'Service', 'Login'))
        self.account_treeview.unbind('<Return>')
        self.account_treeview.bind('<Return>', lambda event: self.select_account_procedure())
        self.account_treeview.bind('<Double-Button-1>', lambda event: self.select_account_procedure())

        self.account_treeview.heading('Nr', text='Nr')
        self.account_treeview.heading('Service', text='Service')
        self.account_treeview.heading('Login', text='Login')

        self.account_treeview.column('Nr', anchor='center', width=40, stretch=False)
        self.account_treeview.column('Service', anchor='center', width=150, stretch=False)
        self.account_treeview.column('Login', anchor='center', width=200, stretch=True)

        self.add_account_button = Button(master=self.display_frame,
                                         text='Add',
                                         command=self.add_account_procedure)
        set_binds_buttons(button=self.add_account_button, command=self.add_account_procedure)

        self.delete_account_button = Button(master=self.display_frame,
                                            text='Delete',
                                            command=self.delete_selected_account_procedure)
        set_binds_buttons(button=self.delete_account_button, command=self.delete_selected_account_procedure)
        self.exit_button = Button(master=self.display_frame,
                                  text='Return',
                                  command=self.return_to_main_window)
        set_binds_buttons(button=self.exit_button, command=self.return_to_main_window)

        self.widget_dict = {1: self.account_treeview,
                            2: self.add_account_button,
                            3: self.delete_account_button,
                            4: self.exit_button}
        self.tab_focus_index_var = IntVar(value=1)

        self.display_frame.place(relx=0.5, rely=0.015, anchor='n')
        self.display_frame.lower(self.main_window_obj.placeholder)
        self.account_treeview.grid(row=0, column=0, columnspan=3, padx=10, pady=5)
        self.add_account_button.grid(row=1, column=0, padx=10, pady=5)
        self.delete_account_button.grid(row=1, column=1, padx=10, pady=5)
        self.exit_button.grid(row=1, column=2, padx=10, pady=5)

        # command used to debug the actions done on the src_file
        # self.root.after(1000, self.file_verification_function)

    def file_verification_function(self):
        if self.src_file:
            with open(self.src_file, 'rb') as file:
                file_data = file.read()

            verificator, encrypted_accounts = file_data.split(b'<0>')
            print(file_data)
            print(encrypted_accounts)
            try:
                decrypted_accounts = decrypt_bytes(encrypted_accounts, self.verified_key).split('<1>')
                print(decrypted_accounts)
            except CipherError:
                print('CipherError')

        self.root.after(1000, self.file_verification_function)

    def fill_tree(self):
        with open(self.src_file, 'rb') as file:
            encrypted_data = file.read()

        verificator, encrypted_accounts = encrypted_data.split(b'<0>')

        if encrypted_accounts:
            try:
                decrypted_accounts = decrypt_bytes(encrypted_accounts, self.verified_key)
                decrypted_accounts = decrypted_accounts.split('<1>')
            except CipherError:
                messagebox.showerror('Error', 'Key passed verification, but failed to decrypt the file. '
                                              'This is most likely caused by the file being corrupted.')
                return

            if decrypted_accounts[0] or True:
                for index, account in enumerate(decrypted_accounts, start=1):
                    try:
                        service, login, password, info = account.split('<2>')
                    except ValueError:
                        continue
                    self.accounts_dict[index] = (service, login, password, info)

                    if service == '<!>':
                        service = ''
                    if login == '<!>':
                        login = ''

                    self.account_treeview.insert(parent='', index='end', values=(index, service, login))

    def empty_tree(self):
        self.account_treeview.delete(*self.account_treeview.get_children())

    def select_account_procedure(self):
        def modify():
            widget_dict_modified = {1: exit_button,
                                    2: modify_button,
                                    3: index_entry,
                                    4: service_entry,
                                    5: login_entry,
                                    6: password_entry,
                                    7: info_textbox}
            tab_focus_index.set(3)
            account_root.bind('<Tab>', lambda event: set_focus_by_index(index_var=tab_focus_index,
                                                                        widget_dict=widget_dict_modified))

            index_entry.configure(state='normal')
            service_entry.configure(state='normal')
            login_entry.configure(state='normal')
            password_entry.configure(state='normal')
            info_textbox.configure(state='normal')
            modify_button.configure(text='Apply Changes', command=apply_changes)
            modify_button.unbind('<FocusIn>')
            set_binds_buttons(button=modify_button, command=apply_changes)

        def close_and_return_to_display_window():
            try:
                index_to_focus = int(index_entry.get())
                if index_to_focus >= len(self.account_treeview.get_children()) or index_to_focus < 1:
                    raise ValueError
            except ValueError:
                index_to_focus = 1

            account_root.destroy()

            self.account_treeview.focus(self.account_treeview.get_children()[index_to_focus - 1])

        def apply_changes():
            try:
                new_index = int(index_entry.get())
                if new_index < 1:
                    raise ValueError
            except ValueError:
                messagebox.showerror('Error', 'Invalid index')
                return

            # you can kill me for this syntax, but I just like it too much
            new_service = service_entry.get() if service_entry.get() else '<!>'
            new_login = login_entry.get() if login_entry.get() else '<!>'
            new_password = password_entry.get() if password_entry.get() else '<!>'
            new_info = info_textbox.get(0.0, 'end').removesuffix('\n') if (
                    info_textbox.get(0.0, 'end').removesuffix('\n') != 'Additional Info') else '<!>'

            new_account_data = f'{new_service}<2>{new_login}<2>{new_password}<2>{new_info}'

            with open(self.src_file, 'rb') as file:
                file_data = file.read()

            verificator, accounts_encrypted = file_data.split(b'<0>')
            accounts_decrypted = decrypt_bytes(accounts_encrypted, self.verified_key).split('<1>')
            accounts_decrypted.pop(selected_index - 1)

            if not new_index or new_index >= len(accounts_decrypted):
                new_index = 'end'

            if new_index == 'end':
                accounts_decrypted.append(new_account_data)
            else:
                accounts_decrypted.insert(new_index - 1, new_account_data)

            accounts_encrypted = verificator + b'<0>' + encrypt_str('<1>'.join(accounts_decrypted), self.verified_key)
            accounts_decrypted = None  # Maybe it will release some RAM in edge cases
            with open(self.src_file, 'wb') as file:
                file.write(accounts_encrypted)

            self.empty_tree()
            self.fill_tree()

            index_entry.configure(state='readonly')
            service_entry.configure(state='readonly')
            login_entry.configure(state='readonly')
            password_entry.configure(state='readonly')
            info_textbox.configure(state='disabled')
            modify_button.configure(text='Modify', command=modify)
            modify_button.unbind('<FocusIn>')
            set_binds_buttons(button=modify_button, command=modify)

            tab_focus_index.set(1)
            account_root.bind('<Tab>', lambda event: set_focus_by_index(index_var=tab_focus_index,
                                                                        widget_dict=widget_dict_normal))

        try:
            selected_item = self.account_treeview.selection()[0]  # It returns ('I004',), so [0] needed
            selected_tuple = self.account_treeview.item(selected_item)
            selected_index = int(selected_tuple["values"][0])
        except ValueError or IndexError:
            return

        service, login, password, info = self.accounts_dict[selected_index]

        account_root = Toplevel(master=self.root)
        account_root.grab_set()
        account_root.bind('<Escape>', lambda event: close_and_return_to_display_window())
        index_entry = Entry(master=account_root,
                            width=40,
                            placeholder_text='index')
        bind_linking_to_keyboard(keyboard_command=self.main_window_obj.keyboard_frame.change_linked_widget,
                                 widget=index_entry)
        index_entry.insert(0, selected_index)
        index_entry.configure(state='readonly')

        service_entry = Entry(master=account_root,
                              width=200,
                              placeholder_text='Service')
        bind_linking_to_keyboard(keyboard_command=self.main_window_obj.keyboard_frame.change_linked_widget,
                                 widget=service_entry)
        service_entry.insert(0, service) if service != '<!>' else None
        service_entry.configure(state='readonly')

        login_entry = Entry(master=account_root,
                            width=200,
                            placeholder_text='Login')
        bind_linking_to_keyboard(keyboard_command=self.main_window_obj.keyboard_frame.change_linked_widget,
                                 widget=login_entry)
        login_entry.insert(0, login) if login != '<!>' else None
        login_entry.configure(state='readonly')

        password_entry = Entry(master=account_root,
                               width=200,
                               placeholder_text='Password')
        bind_linking_to_keyboard(keyboard_command=self.main_window_obj.keyboard_frame.change_linked_widget,
                                 widget=password_entry)
        password_entry.insert(0, password) if password != '<!>' else None
        password_entry.configure(state='readonly')

        info_textbox = Textbox(master=account_root,
                               width=200)
        bind_linking_to_keyboard(keyboard_command=self.main_window_obj.keyboard_frame.change_linked_widget,
                                 widget=info_textbox)
        info_textbox.bind('<FocusIn>', lambda event: toggle_placeholder_on_textbox(textbox=info_textbox,
                                                                                   placeholder='Additional Info',
                                                                                   event=event))
        info_textbox.bind('<FocusOut>', lambda event: toggle_placeholder_on_textbox(textbox=info_textbox,
                                                                                    placeholder='Additional Info',
                                                                                    event=event))
        info_textbox.insert(0.0, info) if info != '<!>' else None
        info_textbox.configure(state='disabled')

        modify_button = Button(master=account_root,
                               text='Modify',
                               command=modify)
        set_binds_buttons(button=modify_button, command=modify)

        exit_button = Button(master=account_root,
                             text='Exit',
                             command=close_and_return_to_display_window)
        set_binds_buttons(button=exit_button, command=close_and_return_to_display_window)

        widget_dict_normal = {1: exit_button,
                              2: modify_button}
        tab_focus_index = IntVar(value=1)

        account_root.bind('<Tab>', lambda event: set_focus_by_index(index_var=tab_focus_index,
                                                                    widget_dict=widget_dict_normal))

        index_entry.grid(row=0, column=0, columnspan=2, padx=10, pady=(5, 0))
        service_entry.grid(row=1, column=0, columnspan=2, padx=10, pady=(5, 0))
        login_entry.grid(row=2, column=0, columnspan=2, padx=10, pady=(5, 0))
        password_entry.grid(row=3, column=0, columnspan=2, padx=10, pady=(5, 0))
        info_textbox.grid(row=4, column=0, columnspan=2, padx=10, pady=(5, 0))
        modify_button.grid(row=5, column=0, padx=10, pady=5)
        exit_button.grid(row=5, column=1, padx=10, pady=5)

    def add_account_procedure(self):
        def close_and_return_to_display_window():
            index_to_focus = index_of_last_added_account.get()

            add_account_root.destroy()

            items_on_treeview = self.account_treeview.get_children()
            self.account_treeview.focus_set()
            self.account_treeview.focus(items_on_treeview[index_to_focus])
            self.account_treeview.selection_set(items_on_treeview[index_to_focus])

        def add_account():
            add_on_number = index_entry.get()
            service = service_entry.get()
            login = login_entry.get()
            password = password_entry.get()
            info = info_textbox.get(0.0, 'end').removesuffix('\n')

            if not add_on_number:
                add_on_index = 'end'
            else:
                try:
                    add_on_index = int(add_on_number) - 1
                    if add_on_index < 0:
                        add_on_index = 0
                except ValueError:
                    messagebox.showerror('Error', 'Invalid Nr.')
                    return
            if not service:
                service = '<!>'
            if not login:
                login = '<!>'
            if not password:
                password = '<!>'
            if not info or info == 'Additional information':
                info = '<!>'

            with open(self.src_file, 'rb') as file:
                data_file = file.read()
            verificator, encrypted_accounts = data_file.split(b'<0>')

            if encrypted_accounts:
                decrypted_accounts = decrypt_bytes(encrypted_accounts, self.verified_key).split('<1>')

                if add_on_index == 'end' or add_on_index >= len(decrypted_accounts):
                    # needed later either way - it is equal to the index of the last item on the treeview
                    # after adding next account
                    add_on_index = len(decrypted_accounts)

                    decrypted_accounts.append(f'{service}<2>{login}<2>{password}<2>{info}')
                else:
                    decrypted_accounts.insert(add_on_index, f'{service}<2>{login}<2>{password}<2>{info}')

            else:
                # called only if the file consists only of the verificator
                decrypted_accounts = [f'{service}<2>{login}<2>{password}<2>{info}']

            encrypted_data_to_write = verificator + b'<0>' + encrypt_str("<1>".join(decrypted_accounts),
                                                                         self.verified_key)
            with open(self.src_file, 'wb') as file:
                file.write(encrypted_data_to_write)

            index_entry.delete(0, 'end')
            service_entry.delete(0, 'end')
            login_entry.delete(0, 'end')
            password_entry.delete(0, 'end')
            info_textbox.delete(0.0, 'end')

            # this is needed for the placeholder_text to work again
            index_entry.focus_set()
            service_entry.focus_set()
            login_entry.focus_set()
            password_entry.focus_set()
            info_textbox.focus_set()
            add_account_root.focus_set()

            self.empty_tree()
            self.fill_tree()

            index_of_last_added_account.set(add_on_index)

        add_account_root = Toplevel(master=self.root)
        add_account_root.grab_set()
        add_account_root.bind('<Escape>', lambda event: close_and_return_to_display_window())
        index_entry = Entry(master=add_account_root,
                            width=40,
                            placeholder_text='index')
        bind_linking_to_keyboard(keyboard_command=self.main_window_obj.keyboard_frame.change_linked_widget,
                                 widget=index_entry)

        service_entry = Entry(master=add_account_root,
                              width=200,
                              placeholder_text='Service')
        bind_linking_to_keyboard(keyboard_command=self.main_window_obj.keyboard_frame.change_linked_widget,
                                 widget=service_entry)

        login_entry = Entry(master=add_account_root,
                            width=200,
                            placeholder_text='Login')
        bind_linking_to_keyboard(keyboard_command=self.main_window_obj.keyboard_frame.change_linked_widget,
                                 widget=login_entry)

        password_entry = Entry(master=add_account_root,
                               width=200,
                               placeholder_text='Password')
        bind_linking_to_keyboard(keyboard_command=self.main_window_obj.keyboard_frame.change_linked_widget,
                                 widget=password_entry)

        info_textbox = Textbox(master=add_account_root,
                               width=200)
        bind_linking_to_keyboard(keyboard_command=self.main_window_obj.keyboard_frame.change_linked_widget,
                                 widget=info_textbox)
        info_textbox.bind('<FocusIn>', lambda event: toggle_placeholder_on_textbox(textbox=info_textbox,
                                                                                   placeholder='Additional Info',
                                                                                   event=event))
        info_textbox.bind('<FocusOut>', lambda event: toggle_placeholder_on_textbox(textbox=info_textbox,
                                                                                    placeholder='Additional Info',
                                                                                    event=event))

        add_button = Button(master=add_account_root,
                            text='Confirm',
                            command=add_account)
        set_binds_buttons(button=add_button, command=add_account)

        exit_button = Button(master=add_account_root,
                             text='Exit',
                             command=close_and_return_to_display_window)
        set_binds_buttons(button=exit_button, command=close_and_return_to_display_window)

        widget_dict = {1: index_entry,
                       2: service_entry,
                       3: login_entry,
                       4: password_entry,
                       5: info_textbox,
                       6: add_button,
                       7: exit_button}
        tab_focus_index = IntVar(value=1)

        index_of_last_added_account = IntVar(value=0)

        add_account_root.bind('<Tab>', lambda event: set_focus_by_index(index_var=tab_focus_index,
                                                                        widget_dict=widget_dict))

        index_entry.grid(row=0, column=0, columnspan=2, padx=10, pady=(5, 0))
        service_entry.grid(row=1, column=0, columnspan=2, padx=10, pady=(5, 0))
        login_entry.grid(row=2, column=0, columnspan=2, padx=10, pady=(5, 0))
        password_entry.grid(row=3, column=0, columnspan=2, padx=10, pady=(5, 0))
        info_textbox.grid(row=4, column=0, columnspan=2, padx=10, pady=(5, 0))
        add_button.grid(row=5, column=0, padx=10, pady=5)
        exit_button.grid(row=5, column=1, padx=10, pady=5)

    def delete_selected_account_procedure(self):
        try:
            selected_item = self.account_treeview.selection()[0]
        except IndexError:
            return
        selected_tuple = self.account_treeview.item(selected_item)
        selected_index = int(selected_tuple["values"][0])

        if not messagebox.askyesno('Confirm', f'Do you relly want to delete '
                                              f'this account (nr: {selected_index})'):
            return

        with open(self.src_file, 'rb') as file:
            file_data = file.read()
        verificator, accounts_encrypted = file_data.split(b'<0>')
        accounts_decrypted = decrypt_bytes(accounts_encrypted, self.verified_key).split('<1>')
        accounts_decrypted.pop(selected_index - 1)

        if accounts_decrypted:
            # note to self: '<1>'.join(accounts_decrypted) returns '<1>' if accounts_decrypted is an empty list
            data_to_write = verificator + b'<0>' + encrypt_str('<1>'.join(accounts_decrypted), self.verified_key)
        else:
            data_to_write = verificator + b'<0>'

        with open(self.src_file, 'wb') as file:
            file.write(data_to_write)

        self.empty_tree()
        self.fill_tree()

        self.account_treeview.focus_set()

        items_left_on_treeview = self.account_treeview.get_children()
        if items_left_on_treeview:
            try:
                self.account_treeview.focus(items_left_on_treeview[selected_index - 1])
                self.account_treeview.selection_set(items_left_on_treeview[selected_index - 1])
            except IndexError:
                # Error risen when deleting the last account on display
                self.account_treeview.focus(items_left_on_treeview[selected_index - 2])
                self.account_treeview.selection_set(items_left_on_treeview[selected_index - 2])

    def return_to_main_window(self):
        self.display_frame.lower(self.main_window_obj.placeholder)
        self.main_window_obj.main_frame.lift()
        self.main_window_obj.keyboard_frame.change_linked_widget(widget=self.main_window_obj.key_entry)
        self.root.bind('<Tab>', lambda: set_focus_by_index(index_var=self.main_window_obj.tab_focus_index,
                                                           widget_dict=self.main_window_obj.widget_dict))
        self.root.unbind('<Delete>')
        self.empty_tree()
