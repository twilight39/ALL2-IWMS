import ttkbootstrap as ttk
from ttkbootstrap.validation import validator, add_validation
import re

# Implements Preview Text for Entry Widgets
class previewText:
    def __init__(self, widget, key, styleObj):

        # Create reference to style object & Identify widget
        self.styleObj = styleObj
        self.key = key

        # Preview Text Dictionary
        self.populateText = {
            "emailEntry" : "abc@companyKEAI.com",
            "passwordEntry" : "abcd1234!"
        }

        # Bind Widget to focus & unfocus operations
        widget.bind("<FocusIn>", lambda event: self.Delete_Text(event))
        widget.bind("<FocusOut>", lambda event: self.Populate_Text(event))

        # Initial Preview Population
        widget.insert(0, self.populateText[self.key])

    def Delete_Text(self, event):
        if str(event.widget.cget("foreground")) == str(self.styleObj.colors.get("secondary")):
            event.widget.delete(0, "end")
            event.widget.configure(foreground="black")

    def Populate_Text(self, event):
        if event.widget.get() == "":
            event.widget.insert(0, self.populateText[self.key])
            event.widget.configure(foreground=self.styleObj.colors.get("secondary"))


# Implements Entry Field Validation
class validation:

    def __init__(self):

        self.errText = {}

        # Validation Type Dictionary
        self.validateType ={
            "email" : validator(self.validateEmail),
            "password" : validator(self.validatePassword)
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

        elif re.match("^[\w\-\.]+@([\w-]+\.)+[\w-]{2,}$", event.postchangetext):
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
