# Imports required libraries
from tkinter import (
    Tk,  # main Tkinter window class
    Label, Button, Frame, PhotoImage,  # Widgets
    BOTH, NSEW, E, LEFT, RIGHT, X  # Positions
)
from tkinter.font import Font
from typing import Literal


# Defines global variables
ICONS = {
    "about": "./icons/about.png",
    "copy": "./icons/copy.png",
}
COLORS = {
    "white"     : "#FFFFFF",
    "off white" : "#f5f5f5",
    "light grey": "#bdbdbd",
    "label"     : "#25265E",
    "light blue": "#CCEDFF",
    "light red" : "#ffcccc",
    "red label" : "#d72121"
}
FONTS = {
    "default": ("Arial", 20),
    "small"  : ("Arial", 16),
    "large"  : ("Arial", 40, "bold"),
    "button" : ("Arial", 24, "bold"),
}


# Main Calculator class controls the GUI and the logic
class Calculator:
    def __init__(self, name: str = "Calculator"):
        self.title = name
        self.app = Tk()
        self.app.geometry("375x667")
        self.app.resizable(False, False)
        self.update_app_title()

        self.header_frame, self.display_frame, self.button_frame = self.create_frames()
        self.total_expression_text = ""
        self.current_expression_text = ""
        self.total_expression_label, self.current_expression_label = self.create_labels()

        self.digits = {
            7  : (1, 0), 8: (1, 1), 9: (1, 2),
            4  : (2, 0), 5: (2, 1), 6: (2, 2),
            1  : (3, 0), 2: (3, 1), 3: (3, 2),
            ".": (4, 0), 0: (4, 1)
        }
        self.create_digit_buttons()
        self.operators = {"/": "\u00F7", "*": "\u00D7", "-": "-", "+": "+"}
        self.create_operator_buttons()
        self.create_special_buttons()
        self.bind_keys()

    # Updates app's title dynamically on call
    def update_app_title(self, subfix: str | None = None):
        title = self.title
        if subfix is not None:
            title = f"{self.title} (R = {subfix})"

        self.app.title(title)

    # Creates two frames for display and buttons
    def create_frames(self):
        frame_header = Frame(self.app, bg=COLORS["light grey"])
        frame_header.pack(fill=X)
        frame_display = Frame(self.app, height=221, bg=COLORS["white"])
        frame_display.pack(fill=BOTH, expand=True)
        frame_button = Frame(self.app)
        frame_button.pack(fill=BOTH, expand=True)

        # Auto-fits available space for all buttons in rows and columns
        for i in range(5):
            frame_button.rowconfigure(i, weight=1)
            frame_button.columnconfigure(i, weight=1) if i != 4 else None

        return frame_header, frame_display, frame_button

    # Creates header
    def create_header(self):
        header_icon = Label(self.header_frame, text="Ico", bg=COLORS["light grey"], fg=COLORS["white"], font=20)
        header_icon.pack(side=LEFT, pady=2, padx=4)
        header_title = Label(self.header_frame, text=self.title)
        header_title.pack(side=LEFT, pady=2)
        about_icon = PhotoImage(file=ICONS["about"])
        copy_icon = PhotoImage(file=ICONS["copy"])
        header_about = Label(self.header_frame, image=about_icon, bg="grey")
        header_about.pack(side=RIGHT,)
        header_copy = Label(self.header_frame, image=copy_icon, borderwidth=0,)
        header_copy.pack(side=RIGHT, pady=2)

    # Creates two labels for the current and total expressions
    def create_labels(self):
        label_total_exp = Label(self.display_frame, text=self.total_expression_text, anchor=E,
                                font=FONTS["small"], bg=COLORS["white"], fg=COLORS["light grey"], padx=24)
        label_total_exp.pack(fill=BOTH, expand=True)
        label_current_exp = Label(self.display_frame, text=self.current_expression_text, anchor=E,
                                  font=FONTS["large"], bg=COLORS["white"], fg=COLORS["label"], padx=24)
        label_current_exp.pack(fill=BOTH, expand=True)

        return label_total_exp, label_current_exp

    # Creates numerical digit buttons with decimal point button
    def create_digit_buttons(self):
        for digit, position in self.digits.items():
            Button(self.button_frame, text=digit, font=FONTS["button"],
                   bg=COLORS["white"] if digit != "." else COLORS["off white"], fg=COLORS["label"],
                   borderwidth=0, command=lambda val=digit: self.update_current_expression_label(val)).grid(
                row=position[0], column=position[1], sticky=NSEW)

    # Creates operator buttons
    def create_operator_buttons(self):
        i = 0
        for operator, symbol in self.operators.items():
            Button(self.button_frame, text=symbol, font=FONTS["default"], bg=COLORS["off white"], fg=COLORS["label"],
                   borderwidth=0, command=lambda val=operator: self.update_total_expression_label(val)).grid(row=i,
                                                                                                             column=3,
                                                                                                             sticky=NSEW)
            i += 1

    # Creates special buttons
    def create_special_buttons(self):
        self.create_equals_clear_buttons()
        self.create_square_sqrt_buttons()

    # Creates equals and clear buttons and called from the above method
    def create_equals_clear_buttons(self):
        Button(self.button_frame, text="C", font=FONTS["default"], bg=COLORS["off white"], fg=COLORS["red label"],
               borderwidth=0, command=self.clear_display).grid(row=0, column=0, sticky=NSEW)
        Button(self.button_frame, text="=", font=FONTS["default"], bg=COLORS["light blue"], fg=COLORS["label"],
               borderwidth=0, command=self.evaluate_total_expression).grid(row=4, column=2, columnspan=2, sticky=NSEW)

    # Creates square and square root buttons
    def create_square_sqrt_buttons(self):
        # Custom font for these two buttons only
        _FONTS = {"italic": Font(family="Times New Roman", size=20, slant="italic")}
        Button(self.button_frame, text="x\u00b2", font=_FONTS["italic"], bg=COLORS["off white"], fg=COLORS["label"],
               borderwidth=0, command=self.current_expression_square_value).grid(row=0, column=1, sticky=NSEW)
        Button(self.button_frame, text="\u221ax", font=_FONTS["italic"], bg=COLORS["off white"], fg=COLORS["label"],
               borderwidth=0, command=self.current_expression_sqrt_value).grid(row=0, column=2, sticky=NSEW)

    # Updates total expression label while invoked
    def update_total_expression_label(self, operator: Literal['/', '*', '-', '+'] | None = None):
        if operator is not None:
            self.current_expression_text += operator
            self.total_expression_text += self.current_expression_text
            self.current_expression_text = ""
            self.update_current_expression_label()

        # Replaces the operators with the symbols in total expression
        total_expression_text = self.total_expression_text
        for operator, symbol in self.operators.items():
            total_expression_text = total_expression_text.replace(operator, f" {symbol} ")
        # Updates the total expression label with the replaced symbols instead of operators
        self.total_expression_label.configure(text=total_expression_text)

    # Updates current expression label while invoked
    def update_current_expression_label(self, value: Literal['.', 0, 1, 2, 3, 4, 5, 6, 7, 8, 9] | None = None):
        if value is not None:
            self.current_expression_text += str(value)
        self.current_expression_label.configure(text=self.current_expression_text)

    # Evaluates the total expression and display the result
    def evaluate_total_expression(self):
        # Appends current expression to the total expression before evaluate
        self.total_expression_text += self.current_expression_text
        self.update_total_expression_label()

        # Calculates the value and display first 12 characters of the result to overcome overflow
        try:
            self.current_expression_text = str(eval(self.total_expression_text))[:12]
            self.update_app_title(self.current_expression_text)
        except ArithmeticError:
            # Displays error on calculation error
            self.current_expression_text = "! Error"
        finally:
            self.update_current_expression_label()

        # Resets the total expression text (without label update)
        # for a new expression again with the evaluated result got
        self.total_expression_text = ""

    # Clears the display (both the total and the current expression labels and texts)
    def clear_display(self):
        self.update_app_title()
        self.current_expression_text = ""
        self.update_current_expression_label()
        self.total_expression_text = ""
        self.update_total_expression_label()

    # Gets current expression's square value
    def current_expression_square_value(self):
        self.current_expression_text = str(eval(f"{self.current_expression_text} ** 2"))
        self.update_current_expression_label()

    # Gets current expression's square root value
    def current_expression_sqrt_value(self):
        self.current_expression_text = str(eval(f"{self.current_expression_text} ** 0.5"))
        self.update_current_expression_label()

    # Binds keys to the number pad, clear and equals buttons
    def bind_keys(self):
        # Binds equals button with the Enter/Return key
        self.app.bind('<Return>', lambda event=None: self.evaluate_total_expression())
        # Binds clear button with the Escape key
        self.app.bind('<Escape>', lambda event=None: self.clear_display())
        # Binds digit buttons with numbers keys
        for digit in self.digits:
            self.app.bind(str(digit), lambda event=None, val=digit: self.update_current_expression_label(val))
        # Binds operator buttons with operator keys
        for operator in self.operators:
            self.app.bind(operator, lambda event=None, val=operator: self.update_total_expression_label(val))

    # Runs the application
    def run(self, icon=None):
        if icon:
            self.app.wm_iconbitmap(icon)
        self.app.mainloop()


# Runs this main.py file for the Calculator application.
if __name__ == '__main__':
    app = Calculator(name="Evaluator")
    app.create_header()
    app.run()
