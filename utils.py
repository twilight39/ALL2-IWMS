import ttkbootstrap as ttk

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
            print(event.widget)

    def Populate_Text(self, event):
        if event.widget.get() == "":
            event.widget.insert(0, self.populateText[self.key])
            event.widget.configure(foreground=self.styleObj.colors.get("secondary"))
