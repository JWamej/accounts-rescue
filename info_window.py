from tkinter import filedialog, messagebox
import customtkinter
from customtkinter import (CTkEntry, CTk, CTkButton, END, CTkTextbox, CTkLabel, CTkToplevel, BooleanVar, IntVar,
                           CTkCheckBox, StringVar, CTkOptionMenu, CTkFrame, WORD)
import info_window_texts

ROOT_BG = 'black'
WIDGET_FG = '#4a0064'
BUTTON_FG = '#650089'
TEXTCOLOR = '#ffffff'
WIDGET_BORDER_COLOR = '#818181'
WIDGET_BORDERWIDTH = 1
FRAME_BG = '#370033'
FONT_NORMAL = ('Arial', 12)
FONT_BIG = ('Arial', 18)


class InfoWindow:
    def __init__(self, master: CTk):
        self.root = CTkToplevel(master=master, fg_color=ROOT_BG)

        self.tutorial_frame = CTkFrame(master=self.root, fg_color=FRAME_BG, border_color=WIDGET_BORDER_COLOR,
                                       border_width=WIDGET_BORDERWIDTH)
        self.faq_frame = CTkFrame(master=self.root, fg_color=FRAME_BG, border_color=WIDGET_BORDER_COLOR,
                                  border_width=WIDGET_BORDERWIDTH)
        self.dosdonts_frame = CTkFrame(master=self.root, fg_color=FRAME_BG, border_color=WIDGET_BORDER_COLOR,
                                       border_width=WIDGET_BORDERWIDTH)

        self.tutorial_label = CTkLabel(master=self.tutorial_frame, text_color=TEXTCOLOR, text='Tutorial', font=FONT_BIG)
        self.tutorial_textbox = CTkTextbox(master=self.tutorial_frame, text_color=TEXTCOLOR, fg_color=WIDGET_FG,
                                           border_color=WIDGET_BORDER_COLOR, border_width=WIDGET_BORDERWIDTH,
                                           font=FONT_NORMAL, width=650, height=420)
        self.tutorial_textbox.insert(0.0, info_window_texts.tutorial_data)
        self.tutorial_textbox.configure(state='disabled')

        self.faq_label = CTkLabel(master=self.faq_frame, text_color=TEXTCOLOR, text='Faq', font=FONT_BIG)
        self.faq_textbox = CTkTextbox(master=self.faq_frame, text_color=TEXTCOLOR, fg_color=WIDGET_FG,
                                      border_color=WIDGET_BORDER_COLOR, border_width=WIDGET_BORDERWIDTH,
                                      font=FONT_NORMAL, width=650, wrap=WORD)
        self.faq_textbox.insert(0.0, info_window_texts.faq)
        self.faq_textbox.configure(state='disabled')

        self.dosdonts_label = CTkLabel(master=self.dosdonts_frame, text_color=TEXTCOLOR, text="Dos and Don'ts",
                                       font=FONT_BIG)
        self.dosdonts_textbox = CTkTextbox(master=self.dosdonts_frame, text_color=TEXTCOLOR, fg_color=WIDGET_FG,
                                           border_color=WIDGET_BORDER_COLOR, border_width=WIDGET_BORDERWIDTH,
                                           font=FONT_NORMAL, width=650, height=140)
        self.dosdonts_textbox.insert(0.0, info_window_texts.dosdonts)
        self.dosdonts_textbox.configure(state='disabled')

        self.exit_button = CTkButton(master=self.root, text='Exit', fg_color=BUTTON_FG, command=self.destroy,
                                     border_width=WIDGET_BORDERWIDTH, border_color=WIDGET_BORDER_COLOR)

    def draw(self):
        self.root.grab_set()
        self.root.focus_set()

        self.tutorial_frame.grid(row=0, column=0, rowspan=2, pady=10, padx=10)
        self.tutorial_label.grid(row=0, column=0, pady=(15, 0), padx=15)
        self.tutorial_textbox.grid(row=1, column=0, pady=(0, 15), padx=15)

        self.faq_frame.grid(row=0, column=1, pady=10, padx=10)
        self.faq_label.grid(row=0, column=0, pady=(15, 0), padx=15)
        self.faq_textbox.grid(row=1, column=0, pady=(0, 15), padx=15, sticky='n')

        self.dosdonts_frame.grid(row=1, column=1, pady=10, padx=10)
        self.dosdonts_label.grid(row=0, column=0, pady=(15, 0), padx=15)
        self.dosdonts_textbox.grid(row=1, column=0, pady=(0, 15), padx=15, sticky='s')

        self.exit_button.grid(row=2, column=0, columnspan=2, pady=(0, 15), padx=15)

    def destroy(self):
        self.root.destroy()
