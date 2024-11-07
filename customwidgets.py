from typing import Any, Literal
from customtkinter import (CTk, CTkToplevel, CTkFrame, CTkLabel, CTkEntry, CTkButton, CTkTextbox, END, WORD, CTkFont,
                           Variable, CTkImage)
from tkinter.ttk import Treeview as TtkTreeview
from tkinter import filedialog, messagebox, Misc
import os
import sys


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
        super().__init__(master = master,
                         fg_color = fg_color)
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

        super().__init__(master = master,
                         width = width,
                         height = height,
                         corner_radius = corner_radius,
                         border_width = border_width,
                         bg_color = bg_color,
                         fg_color = fg_color,
                         border_color = border_color,
                         background_corner_colors = background_corner_colors,
                         overwrite_preferred_drawing_method = overwrite_preferred_drawing_method)


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

        super().__init__(master = master,
                         width = width,
                         height = height,
                         corner_radius = corner_radius,
                         border_width = border_width,
                         border_spacing = border_spacing,
                         bg_color = bg_color,
                         fg_color = fg_color,
                         hover_color = hover_color,
                         border_color = border_color,
                         text_color = text_color,
                         text_color_disabled = text_color_disabled,
                         background_corner_colors = background_corner_colors,
                         round_width_to_even_numbers = round_width_to_even_numbers,
                         round_height_to_even_numbers = round_height_to_even_numbers,
                         text = text,
                         font = font,
                         textvariable = textvariable,
                         image = image,
                         state = state,
                         hover = hover,
                         command = command,
                         compound = compound,
                         anchor = anchor)


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
                 state: str = 'normal'):

        super().__init__(master = master,
                         width = width,
                         height = height,
                         corner_radius = corner_radius,
                         border_width = border_width,
                         bg_color = bg_color,
                         fg_color = fg_color,
                         border_color = border_color,
                         text_color = text_color,
                         placeholder_text_color = placeholder_text_color,
                         textvariable = textvariable,
                         placeholder_text = placeholder_text,
                         font = font,
                         state = state)


class TextBox(CTkTextbox):
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
                 wrap = WORD):

        super().__init__(master = master,
                         width = width,
                         height = height,
                         corner_radius = corner_radius,
                         border_width = border_width,
                         border_spacing = border_spacing,
                         bg_color = bg_color,
                         fg_color = fg_color,
                         border_color = border_color,
                         text_color = text_color,
                         scrollbar_button_color = scrollbar_button_color,
                         scrollbar_button_hover_color = scrollbar_button_hover_color,
                         font = font,
                         activate_scrollbars = activate_scrollbars,
                         wrap = wrap)


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

        super().__init__(master = master,
                         width = width,
                         height = height,
                         corner_radius = corner_radius,
                         bg_color = bg_color,
                         fg_color = fg_color,
                         text_color = text_color,
                         text_color_disabled = text_color_disabled,
                         text = text,
                         font = font,
                         image = image,
                         compound = compound,
                         anchor = anchor,
                         wraplength = wraplength)


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

        super().__init__(master = master,
                         class_ = class_,
                         columns = columns,
                         cursor = cursor,
                         displaycolumns = displaycolumns,
                         height = height,
                         name = name,
                         padding = padding,
                         selectmode = selectmode,
                         show = show,
                         style = style,
                         takefocus = takefocus,
                         xscrollcommand = xscrollcommand,
                         yscrollcommand = yscrollcommand)

        self.tk.call("source", "azure.tcl")
        self.tk.call("set_theme", "dark")


if __name__ == '__main__':
    root = Window()
    frame_test = Frame(master=root)

    label_test = Label(root, text='AAA')
    button_test = Button(root, text='Toplevel', command=lambda: TopLevel(master=root, geometry='500x500', minsize=(500, 500)))
    entry_test = Entry(root, placeholder_text='AAA')
    textbox_text = TextBox(master=frame_test)

    treeview_test = Treeview(master=root, columns=("test1", "test2", "test3"))
    treeview_test.heading("test1", text="test1")
    treeview_test.heading("test2", text="test2")
    treeview_test.heading("test3", text="test3")
    treeview_test.insert("", END, values=(1, "Jan Kowalski", 30))
    treeview_test.insert("", END)
    treeview_test.insert("", END, values=(2, "Anna Nowak", 25))
    treeview_test.insert("", END)
    treeview_test.insert("", END, values=(3, "Marek Wójcik", 35))
    treeview_test.insert("", END)
    treeview_test.insert("", END, values=(1, "Jan Kowalski", 30))
    treeview_test.insert("", END)
    treeview_test.insert("", END, values=(2, "Anna Nowak", 25))
    treeview_test.insert("", END)
    treeview_test.insert("", END, values=(3, "Marek Wójcik", 35))
    treeview_test.insert("", END)
    treeview_test.insert("", END, values=(1, "Jan Kowalski", 30))
    treeview_test.insert("", END)
    treeview_test.insert("", END, values=(2, "Anna Nowak", 25))
    treeview_test.insert("", END)
    treeview_test.insert("", END, values=(3, "Marek Wójcik", 35))
    treeview_test.insert("", END)
    treeview_test.insert("", END, values=(1, "Jan Kowalski", 30))
    treeview_test.insert("", END)
    treeview_test.insert("", END, values=(2, "Anna Nowak", 25))
    treeview_test.insert("", END)
    treeview_test.insert("", END, values=(3, "Marek Wójcik", 35))
    treeview_test.insert("", END)


    label_test.pack(padx=10, pady=10)
    button_test.pack(padx=10, pady=10)
    entry_test.pack(padx=10, pady=10)
    frame_test.pack(padx=10, pady=10)
    textbox_text.pack(padx=10, pady=10)
    treeview_test.pack(padx=10, pady=10)


    root.mainloop()