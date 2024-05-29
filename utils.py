import ttkbootstrap as ttk
import tkinter
from ttkbootstrap.validation import validator, add_validation
import re
import json

from configuration import Configuration

def singleton(cls):
  """Decorator to create a singleton class."""
  instances = {}

  def wrapper(*args, **kwargs):
    if cls not in instances:
      instances[cls] = cls(*args, **kwargs)
    return instances[cls]

  return wrapper

@singleton
class fonts:
    def __init__(self):
        self.fonts = {
            "header1": tkinter.font.Font(family="Zilla Slab", size=50, weight="bold"),
            "header2": tkinter.font.Font(family="Zilla Slab", size=45, weight="bold"),
            "header3": tkinter.font.Font(family="Noto Sans", size=35, weight="bold"),
            "regular": tkinter.font.Font(family="Noto Sans", size=18, weight="bold"),
            "regular2": tkinter.font.Font(family="Inter", size=18, weight="bold"),
            "error": tkinter.font.Font(family="Lexend", size=11, slant="italic")
        }

    def get_font(self, style):
        return self.fonts.get(style.lower(), None)

# Implements Preview Text for Entry Widgets
class previewText:
    def __init__(self, widget, key: str):

        # Create reference to style object & Identify widget
        self.styleObj = ttk.style.Style.get_instance()

        # Get preview text from ui_preview_text.json via key
        config = Configuration()
        with open(config.getPreviewFile(), "r") as f:
            self.previewText = json.load(f).get(key, "")

        # Bind Widget to focus & unfocus operations
        widget.bind("<FocusIn>", lambda event: self.Delete_Text(event))
        widget.bind("<FocusOut>", lambda event: self.Populate_Text(event))

        # Initial Preview Population
        widget.insert(0, self.previewText)
        widget.configure(foreground=self.styleObj.colors.get("secondary"))

    def Delete_Text(self, event):
        if str(event.widget.cget("foreground")) == str(self.styleObj.colors.get("secondary")):
            event.widget.configure(foreground="black")
            if event.widget.get() == self.previewText:
                event.widget.delete(0, "end")

    def Populate_Text(self, event):
        if event.widget.get() == "":
            event.widget.insert(0, self.previewText)
            event.widget.configure(foreground=self.styleObj.colors.get("secondary"))

    @staticmethod
    def initText(key):
        with open("ui_preview_text.json", "r") as f:
            previewText = json.load(f).get(key, "")
        return previewText


# Implements Entry Field Validation
class validation:

    def __init__(self):

        self.errText = {}

        # Validation Type Dictionary
        self.validateType ={
            "email" : validator(self.validateEmail),
            "password" : validator(self.validatePassword),
            "string": validator(self.validateString),
            "price": validator(self.validatePrice),
            "integer": validator(self.validateInteger)
            #"vendor"
        }

    def validate(self, widget, key, errStringVar):

        add_validation(widget, self.validateType[key], when='focusout')
        self.errText[widget] = errStringVar

    def validateEmail(self, event):

        # Empty Field
        if event.postchangetext == "":
            self.errText[event.widget].set("")
            return True

        # -------------------------------------------------------------------------
        # Valid Email Format
        # [\w\-\.] - Local Address (Alphabetical/-/.)
        # @ - @ Symbol
        # ([\w-]+\.)+ - Domain Name (Alphabetical/- + .); can repeat
        # [\w-]{2,} - Top-Level Domain; (Alphabetical/-); min 2 chars
        # -------------------------------------------------------------------------

        elif re.match("^[\w\-.]+@([\w-]+\.)+[\w-]{2,}$", event.postchangetext):
            self.errText[event.widget].set("")
            return True

        # Invalid Email Format
        else:
            self.errText[event.widget].set("Invalid Email Format")
            return False

    def validatePassword(self, event):

        # Empty Field
        if event.postchangetext == "":
            self.errText[event.widget].set("")
            return True

        # Invalid: <8 Characters
        elif len(event.postchangetext) < 8:
            self.errText[event.widget].set("Password must contain at least 8 characters")
            return False

        # Invalid: Contains Invalid Characters
        elif re.search("[^a-zA-Z0-9_\s-]", event.postchangetext) is not None:
            self.errText[event.widget].set("Password may only contain alphanumeric characters")
            return False

        # Invalid: Contains no alphabets
        elif re.search("[a-zA-Z]+", event.postchangetext) is None:
            self.errText[event.widget].set("Password must contain an alphabet")
            return False

        # Invalid: Contains no numbers
        elif re.search("[0-9]+", event.postchangetext) is None:
            self.errText[event.widget].set("Password must contain a number")
            return False

        # Valid
        else:
            self.errText[event.widget].set("")
            return True

    def validateString(self, event):
        # Empty Field
        if event.postchangetext == "":
            self.errText[event.widget].set("")
            return True

        # Invalid: Contains Invalid Characters
        if re.search("[^a-zA-Z0-9_\s-]", event.postchangetext) is not None:
            self.errText[event.widget].set("Only alphanumeric characters allowed.")
            return False

        # Valid
        else:
            self.errText[event.widget].set("")
            return True

    def validatePrice(self, event):
        if event.postchangetext == "":
            self.errText[event.widget].set("")
            return True

        # Valid
        if re.match("^[0-9]+[.[0-9]*]?$", event.postchangetext):
            self.errText[event.widget].set("")
            return True

        # Invalid
        else:
            self.errText[event.widget].set("Only numbers are allowed.")
            return False

    def validateInteger(self, event):
        if event.postchangetext == "":
            self.errText[event.widget].set("")
            return True

        # Valid
        if re.match("^[0-9]+$", event.postchangetext):
            self.errText[event.widget].set("")
            return True

        # Invalid
        else:
            self.errText[event.widget].set("Only integers are allowed.")
            return False

    @staticmethod
    def validateButton(button: ttk.Button, key: list, stringVarList: list) -> bool:
        with open("ui_preview_text.json", "r") as f:
            previewText = json.load(f)
        for i, k in enumerate(key):
            #print(previewText.get(k, ""))
            #print(stringVarList[i].get())
            if previewText.get(k, "") == stringVarList[i].get() or stringVarList[i].get() == "":
                button.configure(state="disabled")
                return False
        return True



if __name__ == "__main__":
    pass