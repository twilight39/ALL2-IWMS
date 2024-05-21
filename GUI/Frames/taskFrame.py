import ttkbootstrap.toast
from pageFrame import *


class taskFrame(pageFrame):

    def __init__(self, master: ttk.Window, role: str) -> None:

        # Inherits Page Frame
        super().__init__(master=master,
                         title="Tasks",
                         role=role,
                         button_config={
                             "Worker": ["Update"],
                             "Supervisor": ["Create", "Update", "Batch Assign", "Delete"],
                             "Administrator": ["Create", "Update", "Batch Assign","Delete"]
                         })

        # Inserts Tableview columns
        colNames = ["Task ID", "Employee Name", "Description", "Progress", "ETA"]
        self._insert_table_headings(colNames)

    def _insert_table_headings(self, colNames:list) -> None:
        for name in colNames:
            self._insert_table_columns(name)

    def getButtonCommand(self, button_text):
        if button_text == "Create":
            self.createPopup()

        elif button_text == "Update":
            self.updatePopup()

        elif button_text == "Batch Assign":
            self.batchPopup()

        elif button_text == "Delete":
            toast = ttkbootstrap.toast.ToastNotification(
                title="Error",
                message="Function is still under development :(",
                duration=3000,
            )
            toast.show_toast()

    def createPopup(self):

        # Creates Popup
        toplevel = popup(master=self.masterWindow, title="Create Task", entryFieldQty=4)

        # Creates Widgets
        toplevel.create_title_frame(frame=toplevel.frameList[0], title="Create Task")
        for index, key in enumerate(["Task ID", "Task Description", "Assigned Employee", "Estimated Time Of Completion"]):
            toplevel.create_label(frame=toplevel.frameList[index+1], label=key)
            toplevel.create_errMsg(frame=toplevel.frameList[index+1], errVar=toplevel.errVar[index])
        for index in range(2):
            toplevel.create_entry(frame=toplevel.frameList[index+1], stringVar=toplevel.stringVar[index])
        toplevel.create_combobox(frame=toplevel.frameList[3], stringVar=toplevel.stringVar[2], options=["Worker A", "Worker B"])
        toplevel.create_entry(frame=toplevel.frameList[4], stringVar=toplevel.stringVar[3])
        toplevel.create_buttonbox(frame=toplevel.frameList[5], command=None)

        # Preview Text
        entryList =["taskDescriptionEntry", "employeeNameEntry", "etaEntry"]
        for index, value in enumerate(entryList):
            previewText(toplevel.entries[index+1], key=value)

        # Validation
        valObj = validation()
        for index in [0, 1, 2, 3]:
            valObj.validate(widget=toplevel.entries[index], key="string", errStringVar=toplevel.errVar[index])

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
        toplevel = popup(master=self.masterWindow, title="Update Task", entryFieldQty=5)

        # Creates Widgets
        toplevel.create_title_frame(frame=toplevel.frameList[0], title="Update Task")
        for index, key in enumerate(
                ["Task ID", "Task Description", "Assigned Employee", "Progress", "Estimated Time Of Completion"]):
            toplevel.create_label(frame=toplevel.frameList[index + 1], label=key)
            toplevel.create_errMsg(frame=toplevel.frameList[index + 1], errVar=toplevel.errVar[index])
        for index in range(2):
            toplevel.create_entry(frame=toplevel.frameList[index + 1], stringVar=toplevel.stringVar[index])
        toplevel.create_combobox(frame=toplevel.frameList[3], stringVar=toplevel.stringVar[2], options=["Worker A", "Worker B"])
        toplevel.create_entry(frame=toplevel.frameList[4], stringVar=toplevel.stringVar[3])
        toplevel.create_combobox(frame=toplevel.frameList[5], stringVar=toplevel.stringVar[4], options=["To-Do", "In Progress", "Completed"])
        toplevel.create_buttonbox(frame=toplevel.frameList[6], command=None)

        # Preview Text
        entryList = ["taskDescriptionEntry", "employeeNameEntry", "progressEntry", "etaEntry"]
        for index, value in enumerate(entryList):
            previewText(toplevel.entries[index + 1], key=value)

        # Validation
        valObj = validation()
        for index in [0, 1, 2, 3, 4]:
            valObj.validate(widget=toplevel.entries[index], key="string", errStringVar=toplevel.errVar[index])

        # Bindings
        toplevel.bind_entry_return()
        toplevel.traceButton(entryList)

        # Configure Frames
        for index in range(1, 6):
            toplevel.configure_frame(frame=toplevel.frameList[index])

        # Grid Frames
        toplevel.configure_toplevel()

    def batchPopup(self):

        # Creates Popup
        toplevel = popup(master=self.masterWindow, title="Batch Assign Tasks", entryFieldQty=6)

        # Creates Widgets
        toplevel.create_title_frame(frame=toplevel.frameList[0], title="Batch Assign Tasks")
        for index, key in enumerate(
                ["Batch ID", "Task 1", "Task 2", "Task 3", "Task 4", "Assigned Employee"]):
            toplevel.create_label(frame=toplevel.frameList[index + 1], label=key)
            toplevel.create_errMsg(frame=toplevel.frameList[index + 1], errVar=toplevel.errVar[index])
        toplevel.create_entry(frame=toplevel.frameList[1], stringVar=toplevel.stringVar[2])
        toplevel.create_combobox(frame=toplevel.frameList[2], stringVar=toplevel.stringVar[2], options=["Task A", "Task B"])
        toplevel.create_combobox(frame=toplevel.frameList[3], stringVar=toplevel.stringVar[3], options=["Task A", "Task B"])
        toplevel.create_combobox(frame=toplevel.frameList[4], stringVar=toplevel.stringVar[4], options=["Task A", "Task B"])
        toplevel.create_combobox(frame=toplevel.frameList[5], stringVar=toplevel.stringVar[5], options=["Task A", "Task B"])
        toplevel.create_buttonbox(frame=toplevel.frameList[6], command=None)

        # Preview Text
        entryList = ["taskDescriptionEntry", "taskDescriptionEntry", "taskDescriptionEntry", "taskDescriptionEntry", "employeeNameEntry"]
        for index, value in enumerate(entryList):
            previewText(toplevel.entries[index ], key=value)

        # Validation
        valObj = validation()
        for index in [0, 1, 2, 3, 4, 5]:
            valObj.validate(widget=toplevel.entries[index], key="string", errStringVar=toplevel.errVar[index])

        # Bindings
        toplevel.bind_entry_return()
        toplevel.traceButton(entryList)

        # Configure Frames
        for index in range(1, 6):
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
    rFrame = taskFrame(window, "Administrator")
    #rFrame.createPopup()

    # Starts Event Main Loop
    window.mainloop()