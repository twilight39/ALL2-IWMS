import ttkbootstrap.toast
from Frames.pageFrame import *

class vendorFrame(pageFrame):

    def __init__(self, master: ttk.Window, role: str) -> None:

        # Inherits Page Frame
        super().__init__(master=master,
                         title="Vendors",
                         role=role,
                         button_config={
                             "Supervisor": ["Add", "Update", "Delete"],
                             "Administrator": ["Add", "Update", "Delete"]
                         })

        # Inserts Tableview columns
        colNames = ["Vendor ID", "Vendor Name", "Email", "Contact Number"]
        self._insert_table_headings(colNames)

    def _insert_table_headings(self, colNames:list) -> None:
        for name in colNames:
            self._insert_table_columns(name)

    def getButtonCommand(self, button_text):
        if button_text == "Add":
            self.addPopup()

        elif button_text == "Update":
            self.updatePopup()

        elif button_text == "Delete":
            toast = ttkbootstrap.toast.ToastNotification(
                title="Error",
                message="Function is still under development :(",
                duration=3000,
            )
            toast.show_toast()

    def addPopup(self):

        # Creates Popup
        toplevel = popup(master=self.masterWindow, title="Add Vendor", entryFieldQty=4)

        # Creates Widgets
        toplevel.create_title_frame(frame=toplevel.frameList[0], title="Add Vendor")
        for index, key in enumerate(["Vendor ID", "Vendor Name", "Email", "Contact Number"]):
            toplevel.create_label(frame=toplevel.frameList[index+1], label=key)
            toplevel.create_errMsg(frame=toplevel.frameList[index+1], errVar=toplevel.errVar[index])
            toplevel.create_entry(frame=toplevel.frameList[index+1], stringVar= toplevel.stringVar[index])
        toplevel.create_buttonbox(frame=toplevel.frameList[5], command=None)

        # Preview Text
        entryList =["vendorNameEntry", "emailEntry", "contactNumberEntry"]
        for index, value in enumerate(entryList):
            previewText(toplevel.entries[index+1], key=value)

        # Validation
        valObj = validation()
        for index in [0, 3]:
            valObj.validate(widget=toplevel.entries[index], key="integer", errStringVar=toplevel.errVar[index])
        valObj.validate(widget=toplevel.entries[1], key="string", errStringVar=toplevel.errVar[1])
        valObj.validate(widget=toplevel.entries[2], key="email", errStringVar=toplevel.errVar[2])

        # Bindings
        toplevel.bind_entry_return()
        toplevel.traceButton(entryList)

        # Configure Frames
        for index in range (1, 5):
            toplevel.configure_frame(frame=toplevel.frameList[index])

        # Grid Frames
        toplevel.configure_toplevel()

    def updatePopup(self):

        # Creates Popup
        toplevel = popup(master=self.masterWindow, title="Update Vendor", entryFieldQty=4)

        # Creates Widgets
        toplevel.create_title_frame(frame=toplevel.frameList[0], title="Update Vendor")
        for index, key in enumerate(["Vendor ID", "Vendor Name", "Email", "Contact Number"]):
            toplevel.create_label(frame=toplevel.frameList[index+1], label=key)
            toplevel.create_errMsg(frame=toplevel.frameList[index+1], errVar=toplevel.errVar[index])
            toplevel.create_entry(frame=toplevel.frameList[index+1], stringVar= toplevel.stringVar[index])
        toplevel.create_buttonbox(frame=toplevel.frameList[5], command=None)

        # Preview Text
        entryList =["vendorNameEntry", "emailEntry", "contactNumberEntry"]
        for index, value in enumerate(entryList):
            previewText(toplevel.entries[index+1], key=value)

        # Validation
        valObj = validation()
        for index in [0, 3]:
            valObj.validate(widget=toplevel.entries[index], key="integer", errStringVar=toplevel.errVar[index])
        valObj.validate(widget=toplevel.entries[1], key="string", errStringVar=toplevel.errVar[1])
        valObj.validate(widget=toplevel.entries[2], key="email", errStringVar=toplevel.errVar[2])

        # Bindings
        toplevel.bind_entry_return()
        toplevel.traceButton(entryList)

        # Configure Frames
        for index in range (1, 5):
            toplevel.configure_frame(frame=toplevel.frameList[index])

        # Grid Frames
        toplevel.configure_toplevel()




# Test Case
if __name__ == "__main__":
    from navigationFrame import navigationFrame

    # Create Main Window, and center it
    window = ttk.Window(title="Keai IWMS", themename="litera", size=(1280, 720))
    ttk.window.Window.place_window_center(window)
    window.rowconfigure(0, weight=1)
    window.columnconfigure(0, weight=1, minsize=200)
    window.columnconfigure(1, weight=20)

    # Creates Frames
    lFrame = navigationFrame(window)
    rFrame = vendorFrame(window, "Administrator")
    #rFrame.createPopup()

    # Starts Event Main Loop
    window.mainloop()