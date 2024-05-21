import ttkbootstrap.toast
from pageFrame import *


class salesOrderFrame(pageFrame):

    def __init__(self, master: ttk.Window, role: str) -> None:

        # Inherits Page Frame
        super().__init__(master=master,
                         title="Sales Order",
                         role=role,
                         button_config={
                             "Supervisor": ["Create", "Add", "Update", "Delete"],
                             "Administrator": ["Create", "Add", "Update", "Delete"]
                         })

        # Inserts Tableview columns
        colNames = ["Sales ID", "Customer Name", "Products Sold", "Quantity", "Serial Number ID", "Date"]
        self._insert_table_headings(colNames)

    def _insert_table_headings(self, colNames:list) -> None:
        for name in colNames:
            self._insert_table_columns(name)

    def getButtonCommand(self, button_text):
        if button_text == "Create":
            self.createPopup()

        elif button_text == "Add":
            self.addPopup()

        elif button_text == "Update":
            toast = ttkbootstrap.toast.ToastNotification(
                title="Error",
                message="Function is still under development :(",
                duration=3000,
            )
            toast.show_toast()

        elif button_text == "Delete":
            toast = ttkbootstrap.toast.ToastNotification(
                title="Error",
                message="Function is still under development :(",
                duration=3000,
            )
            toast.show_toast()

    def createPopup(self):

        # Creates Popup
        toplevel = popup(master=self.masterWindow, title="Create Sales Order", entryFieldQty=4)

        # Creates Widgets
        toplevel.create_title_frame(frame=toplevel.frameList[0], title="Create Sales Order")
        for index, key in enumerate(["Customer ID", "Product ID", "Serial Number ID", "Quantity"]):
            toplevel.create_label(frame=toplevel.frameList[index+1], label=key)
            toplevel.create_errMsg(frame=toplevel.frameList[index+1], errVar=toplevel.errVar[index])
        toplevel.create_combobox(frame=toplevel.frameList[1], stringVar=toplevel.stringVar[0], options=["Customer A", "Customer B"])
        toplevel.create_combobox(frame=toplevel.frameList[2], stringVar=toplevel.stringVar[1], options=["Product A", "Product B"])
        toplevel.create_combobox(frame=toplevel.frameList[3], stringVar=toplevel.stringVar[2], options=["2403-00001", "2403-00002"])
        toplevel.create_entry(frame=toplevel.frameList[4], stringVar=toplevel.stringVar[3])
        toplevel.create_buttonbox(frame=toplevel.frameList[5], command=None)

        # Preview Text
        entryList =["customerIDEntry", "productIDEntry", "serialNumberIDEntry", "quantityEntry"]
        for index, value in enumerate(entryList):
            previewText(toplevel.entries[index], key=value)

        # Validation
        valObj = validation()
        for index in [0, 1, 3]:
            valObj.validate(widget=toplevel.entries[index], key="integer", errStringVar=toplevel.errVar[index])
        valObj.validate(widget=toplevel.entries[2], key="string", errStringVar=toplevel.errVar[2])

        # Bindings
        toplevel.bind_entry_return()
        toplevel.traceButton(entryList)

        # Configure Frames
        for index in range (1, 5):
            toplevel.configure_frame(frame=toplevel.frameList[index])

        # Grid Frames
        toplevel.configure_toplevel()

    def addPopup(self):

        # Creates Popup
        toplevel = popup(master=self.masterWindow, title="Add Sales Order", entryFieldQty=4)

        # Creates Widgets
        toplevel.create_title_frame(frame=toplevel.frameList[0], title="Add Sales Order")
        for index, key in enumerate(["Sales ID", "Product ID", "Serial Number ID", "Quantity"]):
            toplevel.create_label(frame=toplevel.frameList[index+1], label=key)
            toplevel.create_errMsg(frame=toplevel.frameList[index+1], errVar=toplevel.errVar[index])
        toplevel.create_combobox(frame=toplevel.frameList[1], stringVar=toplevel.stringVar[0], options=["Sale ID 1", "Sale ID 2"])
        toplevel.create_combobox(frame=toplevel.frameList[2], stringVar=toplevel.stringVar[1], options=["Product A", "Product B"])
        toplevel.create_combobox(frame=toplevel.frameList[3], stringVar=toplevel.stringVar[2], options=["2403-00001", "2403-00002"])
        toplevel.create_entry(frame=toplevel.frameList[4], stringVar=toplevel.stringVar[3])
        toplevel.create_buttonbox(frame=toplevel.frameList[5], command=None)

        # Preview Text
        entryList =["saleIDEntry", "productIDEntry", "serialNumberIDEntry", "quantityEntry"]
        for index, key in enumerate(entryList):
            previewText(toplevel.entries[index], key=key)

        # Validation
        valObj = validation()
        for index in [0, 1, 3]:
            valObj.validate(widget=toplevel.entries[index], key="integer", errStringVar=toplevel.errVar[index])
        valObj.validate(widget=toplevel.entries[2], key="string", errStringVar=toplevel.errVar[2])

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
    rFrame = salesOrderFrame(window, "Administrator")
    #rFrame.createPopup()

    # Starts Event Main Loop
    window.mainloop()