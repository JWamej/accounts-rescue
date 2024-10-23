from customtkinter import CTkEntry, CTk, CTkToplevel, StringVar, CTkCheckBox


# This is not a part of any other file just to avoid the ImportError (circular import)
class CensorCheckbox:
    def __init__(self, master: CTk | CTkToplevel, entry: CTkEntry, str_var: StringVar, font: tuple, text_color: str):
        self.root = master
        self.entry = entry
        self.censor = str_var
        self.font = font
        self.text_color = text_color

        self.toggle_censor_checkbox = CTkCheckBox(master=self.root, text='Hide', font=font,
                                                  variable=self.censor, onvalue='*', offvalue='',
                                                  text_color=self.text_color,
                                                  command=lambda: (self.entry.configure(show=self.censor.get())))

    def get(self) -> CTkCheckBox:
        return self.toggle_censor_checkbox
