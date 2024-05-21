import ttkbootstrap.toast
from pageFrame import *


class productFrame(pageFrame):

    def __init__(self, master: ttk.Window, role: str) -> None:

        # Inherits Page Frame
        super().__init__(master=master,
                         title="Product",
                         role=role,
                         button_config={
                             "Worker": ["Add", "Update"],
                             "Supervisor": ["Add", "Update"],
                             "Administrator": ["Create", "Add", "Update", "Delete"]
                         })

        # Inserts Tableview columns
        colNames = ["Product ID", "Name", "Description", "Quantity", "Location", "Serial Number ID"]
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
            self.updatePopup()

        elif button_text == "Delete":
            toast = ttkbootstrap.toast.ToastNotification(
                title="Error",
                message="Function is still under development :(",
                duration=3000,
            )
            toast.show_toast()

    def createPopup(self):

        # Creates Popup
        toplevel = popup(master=self.masterWindow, title="Create Product", entryFieldQty=4)

        # Creates Widgets
        toplevel.create_title_frame(frame=toplevel.frameList[0], title="Create Product")
        for index, key in enumerate(["Name", "Description", "Price (RM)", "Preferred Vendor"]):
            toplevel.create_label(frame=toplevel.frameList[index+1], label=key)
            toplevel.create_errMsg(frame=toplevel.frameList[index+1], errVar=toplevel.errVar[index])
        for index in range(3):
            toplevel.create_entry(frame=toplevel.frameList[index+1], stringVar=toplevel.stringVar[index])
        toplevel.create_combobox(frame=toplevel.frameList[4], stringVar=toplevel.stringVar[3], options=["N/A", "Company A", "Company B"])
        toplevel.create_buttonbox(frame=toplevel.frameList[5], command=None)

        # Preview Text
        previewText(toplevel.entries[0], key="productNameEntry")
        previewText(toplevel.entries[1], key="productDescriptionEntry")
        previewText(toplevel.entries[2], key="priceEntry")
        previewText(toplevel.entries[3], key="preferredVendorEntry")

        # Validation
        valObj = validation()
        for index in [0, 1, 3]:
            valObj.validate(widget=toplevel.entries[index], key="string", errStringVar=toplevel.errVar[index])
        valObj.validate(widget=toplevel.entries[2], key="price", errStringVar=toplevel.errVar[2])

        # Bindings
        toplevel.bind_entry_return()
        toplevel.traceButton(["productNameEntry", "productDescriptionEntry", "priceEntry", "preferredVendorEntry"])

        # Configure Frames
        for index in range (1, 5):
            toplevel.configure_frame(frame=toplevel.frameList[index])

        # Grid Frames
        toplevel.configure_toplevel()

    def addPopup(self):

        # Creates Popup
        toplevel = popup(master=self.masterWindow, title="Add Product", entryFieldQty=4)

        # Creates Widgets
        toplevel.create_title_frame(frame=toplevel.frameList[0], title="Add Product")
        for index, key in enumerate(["ProductID", "Quantity", "Location", "Serial Number ID"]):
            toplevel.create_label(frame=toplevel.frameList[index+1], label=key)
            toplevel.create_errMsg(frame=toplevel.frameList[index+1], errVar=toplevel.errVar[index])
        for index in range(4):
            if index == 2:
                toplevel.create_combobox(frame=toplevel.frameList[3], stringVar=toplevel.stringVar[2], options=["Retrieval", "Warehouse", "Packaging", "Delivery"])
            else:
                toplevel.create_entry(frame=toplevel.frameList[index+1], stringVar=toplevel.stringVar[index])

        toplevel.create_buttonbox(frame=toplevel.frameList[5], command=None)

        # Preview Text
        previewText(toplevel.entries[0], key="productIDEntry")
        previewText(toplevel.entries[1], key="quantityEntry")
        previewText(toplevel.entries[2], key="locationEntry")
        previewText(toplevel.entries[3], key="serialNumberIDEntry")

        # Validation
        valObj = validation()
        valObj.validate(widget=toplevel.entries[0], key="string", errStringVar=toplevel.errVar[0])
        valObj.validate(widget=toplevel.entries[1], key="integer", errStringVar=toplevel.errVar[1])
        # Custom database validation required for location and serial number

        # Bindings
        toplevel.bind_entry_return()
        toplevel.traceButton(["productIDEntry", "quantityEntry", "locationEntry", "serialNumberIDEntry"])

        # Configure Frames
        for index in range (1, 5):
            toplevel.configure_frame(frame=toplevel.frameList[index])

        # Grid Frames
        toplevel.configure_toplevel()

    def updatePopup(self):

        # Creates Popup
        toplevel = popup(master=self.masterWindow, title="Update Product", entryFieldQty=3)

        # Creates Widgets
        toplevel.create_title_frame(frame=toplevel.frameList[0], title="Update Product")
        for index, key in enumerate([ "Quantity", "Location"]):
            toplevel.create_label(frame=toplevel.frameList[index+1], label=key)
            toplevel.create_errMsg(frame=toplevel.frameList[index+1], errVar=toplevel.errVar[index])
        for index in range(2):
            if index == 1:
                toplevel.create_combobox(frame=toplevel.frameList[index+1], stringVar=toplevel.stringVar[index], options=["Retrieval", "Warehouse", "Packaging", "Delivery"])
            else:
                toplevel.create_entry(frame=toplevel.frameList[index+1], stringVar=toplevel.stringVar[index])

        toplevel.create_buttonbox(frame=toplevel.frameList[3], command=None)

        # Preview Text
        previewText(toplevel.entries[0], key="quantityEntry")
        previewText(toplevel.entries[1], key="locationEntry")

        # Validation
        valObj = validation()
        valObj.validate(widget=toplevel.entries[0], key="integer", errStringVar=toplevel.errVar[0])
        valObj.validate(widget=toplevel.entries[1], key="string", errStringVar=toplevel.errVar[1])
        # Custom database validation required for location and quantity

        # Bindings
        toplevel.bind_entry_return()
        toplevel.traceButton(["quantityEntry", "locationEntry"])

        # Configure Frames
        for index in range (1, 3):
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
    rFrame = productFrame(window, "Administrator")
    #rFrame.createPopup()

    # Starts Event Main Loop
    window.mainloop()