from typing import Any, Literal
from customtkinter import (CTk, CTkToplevel, CTkFrame, CTkLabel, CTkEntry, CTkButton, CTkTextbox, END, WORD, CTkFont,
                           Variable, CTkImage, StringVar, CTkCheckBox, BooleanVar)
from tkinter.ttk import Treeview as TtkTreeview
from tkinter import filedialog, messagebox, Misc
import os
import sys
import keyboard


DEFAULT_ROOT_FG = 'black'
DEFAULT_FRAME_FG = '#1c0016'
DEFAULT_WIDGET_FG = '#4a0064'
DEFAULT_BUTTON_FG = '#650089'
DEFAULT_BUTTON_HOVER_FG = '#46004c'
DEFAULT_CHECKBOX_CHECKMARK = '#001ea7'
DEFAULT_CHECKBOX_HOVER_FG = '#00115d'
DEFAULT_TEXTCOLOR = '#ffffff'
DEFAULT_TEXTCOLOR_DISABLED = '#818181'
DEFAULT_TEXTCOLOR_PLACEHOLDER = DEFAULT_TEXTCOLOR_DISABLED
DEFAULT_BORDER_COLOR = '#4c4c4c'
DEFAULT_BORDERWIDTH = 1
FONT_NORMAL = ('Arial', 12)
FONT_BIG = ('Arial', 18)


class Window(CTk):
    def __init__(self,
                 fg_color: str = DEFAULT_ROOT_FG,
                 geometry: str = None,
                 min_size: tuple[int, int] = (50, 50),
                 title: str = 'Root'):
        super().__init__(fg_color=fg_color)
        self.geometry(geometry)
        self.minsize(min_size[0], min_size[1])
        self.title(title)


class TopLevel(CTkToplevel):
    def __init__(self,
                 master: Any = None,
                 fg_color: str = DEFAULT_ROOT_FG,
                 geometry: str = None,
                 minsize: tuple[int, int] = (0, 0)):
        super().__init__(master=master,
                         fg_color=fg_color)
        self.geometry(geometry)
        self.minsize(width=minsize[0], height=minsize[1])


class Frame(CTkFrame):
    def __init__(self,
                 master: Any,
                 width: int = 200,
                 height: int = 200,
                 corner_radius: int | str | None = None,
                 border_width: int | str | None = DEFAULT_BORDERWIDTH,
                 bg_color: str | tuple[str, str] = "transparent",
                 fg_color: str | tuple[str, str] | None = DEFAULT_FRAME_FG,
                 border_color: str | tuple[str, str] | None = DEFAULT_BORDER_COLOR,
                 background_corner_colors: tuple[str | tuple[str, str]] | None = None,
                 overwrite_preferred_drawing_method: str | None = None):

        super().__init__(master=master,
                         width=width,
                         height=height,
                         corner_radius=corner_radius,
                         border_width=border_width,
                         bg_color=bg_color,
                         fg_color=fg_color,
                         border_color=border_color,
                         background_corner_colors=background_corner_colors,
                         overwrite_preferred_drawing_method=overwrite_preferred_drawing_method)


class KeyboardFrame(CTkFrame):
    def __init__(self,
                 master: Any,
                 write_on: CTkEntry | CTkTextbox,
                 width: int = 200,
                 height: int = 200,
                 size_multiplier: float = 1,
                 font: tuple | CTkFont | None = FONT_NORMAL,
                 corner_radius: int | str | None = None,
                 border_width: int | str | None = None,
                 bg_color: str | tuple[str, str] = "transparent",
                 fg_color: str | tuple[str, str] | None = None,
                 border_color: str | tuple[str, str] | None = None,
                 background_corner_colors: tuple[str | tuple[str, str]] | None = None,
                 overwrite_preferred_drawing_method: str | None = None):
        super().__init__(master=master,
                         width=width,
                         height=height,
                         corner_radius=corner_radius,
                         border_width=border_width,
                         bg_color=bg_color,
                         fg_color=fg_color,
                         border_color=border_color,
                         background_corner_colors=background_corner_colors,
                         overwrite_preferred_drawing_method=overwrite_preferred_drawing_method)
        self.size_multiplier = size_multiplier
        self.font = font
        self.linked_widged = write_on
        self.shift_on = BooleanVar(value=False)
        self.caps_on = BooleanVar(value=False)
        self.default_chars = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '-', '=', '`', 'q', 'w', 'e', 'r', 't',
                              'y', 'u', 'i', 'o', 'p', '[', ']', '\\', 'a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l', '/',
                              ';', "'", 'z', 'x', 'c', 'v', 'b', 'n', 'm', ',', '.']
        self.shifted_chars = ['!', '@', '#', '$', '%', '^', '&', '*', '(', ')', '_', '+', '~', 'Q', 'W', 'E', 'R', 'T',
                            'Y', 'U', 'I', 'O', 'P', '{', '}', '|', 'A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L', '?',
                            ':', '"', 'Z', 'X', 'C', 'V', 'B', 'N', 'M', '<', '>']
        self.buttons_shiftable_list = []
        self.buttons_draw()

    def buttons_draw(self):
        grid_place = [0, 0]
        column_max = 30
        size = int(30 * self.size_multiplier)  # Keep in mind that float-input makes the layout really irregular

        # Loop that grids all buttons except: spacebar, capslock, shift, backspace, arrows
        for index in range(47):
            button = Button(master=self,
                            text=self.default_chars[index],
                            width=int(size),
                            font=self.font)
            button.configure(hover_color=DEFAULT_BUTTON_FG,
                             command=lambda t=self.default_chars[index]: self.normal_on_click(character=t))
            self.buttons_shiftable_list.append(button)

            # looks weird, but works
            if grid_place == [0, 0] or grid_place == [0, 1]:
                padx = (5, 1)
            elif grid_place == [1, 2]:
                padx = (3, 1)
            elif grid_place == [28, 0] or grid_place == [28, 1] or grid_place == [28, 2] or grid_place == [28, 3]:
                padx = (1, 5)
            else:
                padx = 1

            if grid_place[1] == 0:
                pady = (5, 1)
            else:
                pady = 1

            button.grid(row=grid_place[1], column=grid_place[0], columnspan=2, padx=padx, pady=pady)

            grid_place[0] += 2

            # moves the buttons to a new row when needed
            if grid_place[0] >= column_max:
                if grid_place[1] == 0:
                    grid_place = [0, 1]
                elif grid_place[1] == 1:
                    grid_place = [1, 2]
                elif grid_place[1] == 2:
                    grid_place = [3, 3]

            # creates place for other buttons that are not gridded in this loop
            elif grid_place == [20, 0]:
                grid_place = [24, 0]

            elif grid_place == [20, 1]:
                grid_place = [24, 1]

            elif grid_place == [19, 2]:
                grid_place = [24, 2]

            elif grid_place == [17, 3]:
                grid_place = [24, 3]

            elif grid_place == [26, 3]:
                grid_place = [28, 3]

        backspace = Button(master=self,
                           text='<==',
                           width=int(2 * size),
                           hover_color=DEFAULT_BUTTON_FG,
                           font=self.font,
                           command=self.backspace_on_click)

        capslock = Button(master=self,
                          text='caps',
                          width=int(2 * size),
                          hover_color=DEFAULT_BUTTON_FG,
                          font=self.font,
                          command=self.capslock_on_click)

        enter = Button(master=self,
                       text='enter',
                       width=int(2.5 * size + 1),
                       hover_color=DEFAULT_BUTTON_FG,
                       font=self.font,
                       command=self.enter_on_click)

        shift = Button(master=self,
                       text='shift',
                       width=int(3.5 * size + 3),
                       hover_color=DEFAULT_BUTTON_FG,
                       font=self.font,
                       command=self.toggle_shift_on_click)

        spacebar = Button(master=self,
                          text='space',
                          width=int(5 * size + 8),
                          hover_color=DEFAULT_BUTTON_FG,
                          font=self.font,
                          command=self.spacebar_on_click)

        arrow_up = Button(master=self,
                          text='↑',
                          width=int(size),
                          hover_color=DEFAULT_BUTTON_FG,
                          font=self.font,
                          command=lambda: self.arrow_on_click(0, 1))

        arrow_left = Button(master=self,
                            text='←',
                            width=int(size),
                            hover_color=DEFAULT_BUTTON_FG,
                            font=self.font,
                            command=lambda: self.arrow_on_click(-1, 0))

        arrow_down = Button(master=self,
                            text='↓',
                            width=int(size),
                            hover_color=DEFAULT_BUTTON_FG,
                            font=self.font,
                            command=lambda: self.arrow_on_click(0, -1))

        arrow_right = Button(master=self,
                             text='→',
                             width=int(size),
                             hover_color=DEFAULT_BUTTON_FG,
                             font=self.font,
                             command=lambda: self.arrow_on_click(1, 0))

        backspace.grid(row=0, column=20, columnspan=4, padx=1, pady=(5, 1))
        capslock.grid(row=1, column=20, columnspan=4, padx=1, pady=1)
        enter.grid(row=2, column=19, columnspan=5, padx=1, pady=1)
        shift.grid(row=3, column=17, columnspan=7, padx=1, pady=1)
        spacebar.grid(row=4, column=5, columnspan=10, pady=(1, 5))
        arrow_up.grid(row=3, column=26, padx=1, pady=1)
        arrow_left.grid(row=4, column=24, padx=1, pady=(1, 5))
        arrow_down.grid(row=4, column=26, padx=1, pady=(1, 5))
        arrow_right.grid(row=4, column=28, padx=(1, 5), pady=(1, 5))

    def normal_on_click(self, character: str, *args):
        position = self.linked_widged.index('insert')

        # ?There is a glitch that if the shift is pressed on the normal keyboard, it starts to work only after 2nd input
        if self.shift_on.get() or self.caps_on.get() or keyboard.is_pressed('shift'):
            character = self.shifted_chars[self.default_chars.index(character)]
            self.linked_widged.insert(position, character)

            if self.shift_on.get():
                self.toggle_shift_on_click()
            return
        self.linked_widged.insert(position, character)

    def backspace_on_click(self):
        # without this check one can start deleting entry's placeholder text by clicking backspace
        if not self.linked_widged.get():
            return

        if isinstance(self.linked_widged, Entry):
            x = self.linked_widged.index('insert')
            self.linked_widged.delete(int(x) - 1)

        elif isinstance(self.linked_widged, Textbox):
            y, x = self.linked_widged.index('insert').split('.')
            self.linked_widged.delete(f'{y}.{int(x) - 1}')

    def capslock_on_click(self):
        if self.caps_on.get():
            self.caps_on.set(False)
            self.change_upper_lowercase(lowercase=True)
            return
        self.caps_on.set(True)
        self.change_upper_lowercase(lowercase=False)

    # could cause some problems, because it doesn't insert the 'enter' directly, instead it
    # imitates the 'enter' key-press
    def enter_on_click(self):
        keyboard.press('enter')

    def toggle_shift_on_click(self):
        # with caps turned on, the shift should have no effect and without that logic, the whole lower-, uppercase
        # letter system goes tits up
        if not self.caps_on.get():
            if self.shift_on.get():
                self.shift_on.set(False)
                self.change_upper_lowercase(lowercase=True)
                return

            self.change_upper_lowercase(lowercase=False)
            self.shift_on.set(True)

    def arrow_on_click(self, change_horizontal: int = 0, change_vertical: int = 0):
        if isinstance(self.linked_widged, Entry):
            x = self.linked_widged.index('insert')
            self.linked_widged.icursor(f'{x + change_horizontal}')
        elif isinstance(self.linked_widged, Textbox):
            y, x = self.linked_widged.index('insert').split('.')

            # this cursed line is used to move cursor on the Textbox, because icursor doesn't work on Textboxes
            self.linked_widged.mark_set('insert', '%d.%d' % (int(y) - change_vertical, int(x) + change_horizontal))

    def spacebar_on_click(self):
        self.linked_widged.insert(self.linked_widged.index('insert'), ' ')

    def change_upper_lowercase(self, lowercase: bool):
        if lowercase:
            for index, button in enumerate(self.buttons_shiftable_list):
                button.configure(text=self.default_chars[index])
            return
        for index, button in enumerate(self.buttons_shiftable_list):
            button.configure(text=self.shifted_chars[index])

    def change_linked_widget(self, widget: CTkEntry | CTkTextbox):
        self.linked_widged = widget


class Button(CTkButton):
    def __init__(self,
                 master: Any,
                 width: int = 140,
                 height: int = 28,
                 corner_radius: int | None = None,
                 border_width: int | None = DEFAULT_BORDERWIDTH,
                 border_spacing: int = 2,
                 bg_color: str | tuple[str, str] = "transparent",
                 fg_color: str | tuple[str, str] | None = DEFAULT_BUTTON_FG,
                 hover_color: str | tuple[str, str] | None = DEFAULT_BUTTON_HOVER_FG,
                 border_color: str | tuple[str, str] | None = DEFAULT_BORDER_COLOR,
                 text_color: str | tuple[str, str] | None = DEFAULT_TEXTCOLOR,
                 text_color_disabled: str | tuple[str, str] | None = DEFAULT_TEXTCOLOR_DISABLED,
                 background_corner_colors: tuple[str | tuple[str, str]] | None = None,
                 round_width_to_even_numbers: bool = True,
                 round_height_to_even_numbers: bool = True,
                 text: str = 'Button',
                 font: tuple | CTkFont | None = FONT_NORMAL,
                 textvariable: Variable | None = None,
                 image: CTkImage | None = None,
                 state: str = "normal",
                 hover: bool = True,
                 command: () = None,
                 compound: str = "left",
                 anchor: str = "center"):

        super().__init__(master=master,
                         width=width,
                         height=height,
                         corner_radius=corner_radius,
                         border_width=border_width,
                         border_spacing=border_spacing,
                         bg_color=bg_color,
                         fg_color=fg_color,
                         hover_color=hover_color,
                         border_color=border_color,
                         text_color=text_color,
                         text_color_disabled=text_color_disabled,
                         background_corner_colors=background_corner_colors,
                         round_width_to_even_numbers=round_width_to_even_numbers,
                         round_height_to_even_numbers=round_height_to_even_numbers,
                         text=text,
                         font=font,
                         textvariable=textvariable,
                         image=image,
                         state=state,
                         hover=hover,
                         command=command,
                         compound=compound,
                         anchor=anchor)


class Entry(CTkEntry):
    def __init__(self,
                 master: Any,
                 width: int = 140,
                 height: int = 28,
                 corner_radius: int | None = None,
                 border_width: int | None = DEFAULT_BORDERWIDTH,
                 bg_color: str | tuple[str, str] = "transparent",
                 fg_color: str | tuple[str, str] | None = DEFAULT_WIDGET_FG,
                 border_color: str | tuple[str, str] | None = DEFAULT_BORDER_COLOR,
                 text_color: str | tuple[str, str] | None = DEFAULT_TEXTCOLOR,
                 placeholder_text_color: str | tuple[str, str] | None = DEFAULT_TEXTCOLOR_PLACEHOLDER,
                 textvariable: Variable | None = None,
                 placeholder_text: str | None = None,
                 font: tuple | CTkFont | None = FONT_NORMAL,
                 state: str = 'normal',
                 show: str | int = None):

        super().__init__(master=master,
                         width=width,
                         height=height,
                         corner_radius=corner_radius,
                         border_width=border_width,
                         bg_color=bg_color,
                         fg_color=fg_color,
                         border_color=border_color,
                         text_color=text_color,
                         placeholder_text_color=placeholder_text_color,
                         textvariable=textvariable,
                         placeholder_text=placeholder_text,
                         font=font,
                         state=state,
                         show=show)


class Textbox(CTkTextbox):
    def __init__(self,
                 master: Any,
                 width: int = 200,
                 height: int = 200,
                 corner_radius: int | None = None,
                 border_width: int | None = DEFAULT_BORDERWIDTH,
                 border_spacing: int = 3,
                 bg_color: str | tuple[str, str] = "transparent",
                 fg_color: str | tuple[str, str] | None = DEFAULT_WIDGET_FG,
                 border_color: str | tuple[str, str] | None = DEFAULT_BORDER_COLOR,
                 text_color: str | None = DEFAULT_TEXTCOLOR,
                 scrollbar_button_color: str | tuple[str, str] | None = None,
                 scrollbar_button_hover_color: str | tuple[str, str] | None = None,
                 font: tuple | CTkFont | None = FONT_NORMAL,
                 activate_scrollbars: bool = True,
                 wrap=WORD):

        super().__init__(master=master,
                         width=width,
                         height=height,
                         corner_radius=corner_radius,
                         border_width=border_width,
                         border_spacing=border_spacing,
                         bg_color=bg_color,
                         fg_color=fg_color,
                         border_color=border_color,
                         text_color=text_color,
                         scrollbar_button_color=scrollbar_button_color,
                         scrollbar_button_hover_color=scrollbar_button_hover_color,
                         font=font,
                         activate_scrollbars=activate_scrollbars,
                         wrap=wrap)


class Label(CTkLabel):
    def __init__(self,
                 master: Any,
                 width: int = 0,
                 height: int = 28,
                 corner_radius: int | None = None,
                 bg_color: str | tuple[str, str] = "transparent",
                 fg_color: str | tuple[str, str] | None = None,
                 text_color: str | tuple[str, str] | None = DEFAULT_TEXTCOLOR,
                 text_color_disabled: str | tuple[str, str] | None = DEFAULT_TEXTCOLOR_DISABLED,
                 text: str = "Label",
                 font: tuple | CTkFont | None = FONT_NORMAL,
                 image: CTkImage | None = None,
                 compound: str = "center",
                 anchor: str = "center",
                 wraplength: int = 0):

        super().__init__(master=master,
                         width=width,
                         height=height,
                         corner_radius=corner_radius,
                         bg_color=bg_color,
                         fg_color=fg_color,
                         text_color=text_color,
                         text_color_disabled=text_color_disabled,
                         text=text,
                         font=font,
                         image=image,
                         compound=compound,
                         anchor=anchor,
                         wraplength=wraplength)


class Treeview(TtkTreeview):
    def __init__(self,
                 master: Misc | None = None,
                 class_: str = None,
                 columns: str | list[str] | list[int] | list[str | int] | tuple[str | int, ...] = None,
                 cursor: Any = None,
                 displaycolumns: str | int | list[str] | tuple[str, ...] | list[int] | tuple[int, ...] = None,
                 height: int = None,
                 name: str = None,
                 padding: Any = None,
                 selectmode: Literal["extended", "browse", "none"] = "extended",
                 show: Literal["tree", "headings", "tree headings", ""] | list[str] | tuple[str, ...] = 'headings',
                 style: str = None,
                 takefocus: Any = None,
                 xscrollcommand: Any = None,
                 yscrollcommand: Any = None):

        super().__init__(master=master,
                         class_=class_,
                         columns=columns,
                         cursor=cursor,
                         displaycolumns=displaycolumns,
                         height=height,
                         name=name,
                         padding=padding,
                         selectmode=selectmode,
                         show=show,
                         style=style,
                         takefocus=takefocus,
                         xscrollcommand=xscrollcommand,
                         yscrollcommand=yscrollcommand)

        self.tk.call("source", "azure.tcl")
        self.tk.call("set_theme", "dark")


class CheckBox(CTkCheckBox):
    def __init__(self,
                 master: Any,
                 width: int = 100,
                 height: int = 24,
                 checkbox_width: int = 20,
                 checkbox_height: int = 20,
                 corner_radius: int | None = None,
                 border_width: int | None = None,
                 bg_color: str | tuple[str, str] = "transparent",
                 fg_color: str | tuple[str, str] | None = DEFAULT_WIDGET_FG,
                 hover_color: str | tuple[str, str] | None = DEFAULT_BUTTON_HOVER_FG,
                 border_color: str | tuple[str, str] | None = DEFAULT_BORDER_COLOR,
                 checkmark_color: str | tuple[str, str] | None = None,
                 text_color: str | tuple[str, str] | None = DEFAULT_TEXTCOLOR,
                 text_color_disabled: str | tuple[str, str] | None = DEFAULT_TEXTCOLOR_DISABLED,
                 text: str = "CTkCheckBox",
                 font: tuple | CTkFont | None = FONT_NORMAL,
                 textvariable: Variable | None = None,
                 state: str = 'normal',
                 hover: bool = True,
                 command: () = None,
                 onvalue: int | str = 1,
                 offvalue: int | str = 0,
                 variable: Variable | None = None):
        super().__init__(master=master,
                         width=width,
                         height=height,
                         checkbox_width=checkbox_width,
                         checkbox_height=checkbox_height,
                         corner_radius=corner_radius,
                         border_width=border_width,
                         bg_color=bg_color,
                         fg_color=fg_color,
                         hover_color=hover_color,
                         border_color=border_color,
                         checkmark_color=checkmark_color,
                         text_color=text_color,
                         text_color_disabled=text_color_disabled,
                         text=text,
                         font=font,
                         textvariable=textvariable,
                         state=state,
                         hover=hover,
                         command=command,
                         onvalue=onvalue,
                         offvalue=offvalue,
                         variable=variable)


class CensorCheckbox(CTkCheckBox):
    def __init__(self,
                 master: Any,
                 entry: Entry,
                 str_var: StringVar,
                 width: int = 65,
                 height: int = 24,
                 checkbox_width: int = 18,
                 checkbox_height: int = 18,
                 corner_radius: int | None = None,
                 border_width: int | None = DEFAULT_BORDERWIDTH,
                 bg_color: str | tuple[str, str] = "transparent",
                 fg_color: str | tuple[str, str] | None = DEFAULT_BUTTON_FG,
                 hover_color: str | tuple[str, str] | None = DEFAULT_BUTTON_HOVER_FG,
                 border_color: str | tuple[str, str] | None = DEFAULT_BORDER_COLOR,
                 checkmark_color: str | tuple[str, str] | None = None,
                 text_color: str | tuple[str, str] | None = DEFAULT_TEXTCOLOR,
                 text_color_disabled: str | tuple[str, str] | None = DEFAULT_TEXTCOLOR_DISABLED,
                 text: str = "Show",
                 font: tuple | CTkFont | None = FONT_NORMAL,
                 textvariable: Variable | None = None,
                 state: str = 'normal',
                 hover: bool = True,
                 onvalue: int | str = '',
                 offvalue: int | str = '*'):

        super().__init__(master=master,
                         width=width,
                         height=height,
                         checkbox_width=checkbox_width,
                         checkbox_height=checkbox_height,
                         corner_radius=corner_radius,
                         border_width=border_width,
                         bg_color=bg_color,
                         fg_color=fg_color,
                         hover_color=hover_color,
                         border_color=border_color,
                         checkmark_color=checkmark_color,
                         text_color=text_color,
                         text_color_disabled=text_color_disabled,
                         text=text,
                         font=font,
                         textvariable=textvariable,
                         state=state,
                         hover=hover,
                         command=lambda: (entry.configure(show=str_var.get())),
                         onvalue=onvalue,
                         offvalue=offvalue,
                         variable=str_var)


if __name__ == '__main__':
    root = Window()
    frame_test = Frame(master=root)

    label_test = Label(root, text='AAA')
    button_test = Button(root, text='Toplevel',
                         command=lambda: TopLevel(master=root,
                                                  geometry='500x500',
                                                  minsize=(500, 500)))
    entry_test = Entry(root,
                       placeholder_text='AAA')
    checkbox_test = CheckBox(root, text='Test')
    textbox_text = Textbox(master=frame_test)

    treeview_test = Treeview(master=root, columns=("test1", "test2", "test3"))
    treeview_test.heading("test1", text="test1")
    treeview_test.heading("test2", text="test2")
    treeview_test.heading("test3", text="test3")

    # label_test.pack(padx=10, pady=10)
    # button_test.pack(padx=10, pady=10)
    # entry_test.pack(padx=10, pady=10)
    checkbox_test.pack()
    frame_test.pack(padx=10, pady=10)
    textbox_text.pack(padx=10, pady=10)
    # treeview_test.pack(padx=10, pady=10)

    keyboard_frame = KeyboardFrame(master=root, size_multiplier=1, write_on=textbox_text)
    keyboard_frame.pack()

    root.mainloop()
