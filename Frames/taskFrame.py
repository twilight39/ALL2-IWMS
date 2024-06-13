import ttkbootstrap.toast
from Frames.pageFrame import *


class taskFrame(pageFrame):

    def __init__(self, master: ttk.Window, role: str) -> None:

        # Inherits Page Frame
        super().__init__(master=master,
                         title="Tasks",
                         role=role,
                         button_config={
                             "Worker": ["Update"],
                             "Supervisor": ["Create", "Update", "Batch Assign", "Delete"],
                             "Administrator": ["Create", "Update", "Batch Assign", "Delete"]
                         })

        # Inserts Tableview columns
        colNames = ["Task ID", "Task Batch", "Employee Name", "Description", "Progress", "ETA"]
        self._insert_table_headings(colNames)

        self.db_connection = DatabaseConnection()
        self._load_table_rows(self.db_connection.query_task_table())

    def _insert_table_headings(self, colNames: list) -> None:
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
            self.deletePopup()

    def createPopup(self):

        def onSubmitButton():
            if not self.db_connection.add_task(description=toplevel.stringVar[0].get(), eta=toplevel.stringVar[2].get(),
                                               worker_id=toplevel.stringVar[1].get().split(' -')[0]):
                toplevel.errVar[4].set("Submission failed to process")
            else:
                self._load_table_rows(self.db_connection.query_task_table())
                toplevel.destroy()

        def validateWorker(event):
            #print(f"{event.postchangetext}\n{event.widget.cget('value')}")
            if event.postchangetext == "" or event.postchangetext == "Employee Name":
                toplevel.errVar[1].set("")
                return True
            elif event.postchangetext not in event.widget.cget("value"):
                toplevel.errVar[1].set("Invalid Employee")
                return False
            else:
                toplevel.errVar[1].set("")
                return True

        def validateDate(event):
            if re.match(r"^\d{4}-\d{2}-\d{2}$", event.postchangetext) is not None or event.postchangetext == "":
                toplevel.errVar[2].set("")
                return True
            else:
                toplevel.errVar[2].set("Invalid Date")
                return False

        # Creates Popup
        toplevel = popup(master=self.masterWindow, title="Create Task", entryFieldQty=3)

        # Creates Widgets
        toplevel.create_title_frame(frame=toplevel.frameList[0], title="Create Task")
        for index, key in enumerate(["Task Description", "Assigned Employee", "Estimated Time Of Completion"]):
            toplevel.create_label(frame=toplevel.frameList[index + 1], label=key)
            toplevel.create_errMsg(frame=toplevel.frameList[index + 1], errVar=toplevel.errVar[index])
        toplevel.create_entry(frame=toplevel.frameList[1], stringVar=toplevel.stringVar[0])
        toplevel.create_combobox(frame=toplevel.frameList[2], stringVar=toplevel.stringVar[1],
                                 options=self.db_connection.query_worker())
        toplevel.create_dateEntry(frame=toplevel.frameList[3], stringVar=toplevel.stringVar[2])
        toplevel.create_buttonbox(frame=toplevel.frameList[4])
        toplevel.submitButton.configure(command=lambda: onSubmitButton(), state='enabled')

        # Preview Text
        entryList = ["taskDescriptionEntry", "employeeNameEntry", "etaEntry"]
        for index, value in enumerate(entryList):
            previewText(toplevel.entries[index], key=value)

        # Validation
        add_validation(toplevel.entries[1], validator(validateWorker), when="focus")
        add_validation(toplevel.entries[2], validator(validateDate), when="focus")

        # Bindings
        toplevel.bind_entry_return()
        #toplevel.traceButton()

        # Configure Frames
        for index in range(1, 4):
            toplevel.configure_frame(frame=toplevel.frameList[index])

        # Grid Frames
        toplevel.configure_toplevel()

    def updatePopup(self):

        def onSubmitButton():
            if not self.db_connection.update_task(
                    task_id=toplevel.stringVar[0].get().split(' - ')[0],
                    description=toplevel.stringVar[0].get().split(' - ')[1],
                    batch_no=toplevel.stringVar[1].get(),
                    worker_id=toplevel.stringVar[2].get().split(' - ')[0],
                    progress=toplevel.stringVar[3].get(),
                    eta=toplevel.stringVar[4].get()):
                toplevel.errVar[5].set("Submission failed to process")
            else:
                self._load_table_rows(self.db_connection.query_task_table())
                toplevel.destroy()

        def onTaskEntry(*args, **kwargs):
            if toplevel.stringVar[0].get() in toplevel.entries[0].cget("value"):
                print([value for value in updatables if value[0] == toplevel.stringVar[0].get()][0])
                details = [value for value in updatables if value[0] == toplevel.stringVar[0].get()][0]
                for i in range(1, 5):
                    toplevel.stringVar[i].set(details[i])
                toplevel.entries[1].configure(state='enabled', foreground="black",
                                              value=self.db_connection.query_taskBatch())
                toplevel.entries[2].configure(state='enabled', value=self.db_connection.query_worker(),
                                              foreground="black")
                toplevel.entries[3].configure(state='enabled', value=['Not Started', 'In Progress', 'Completed'],
                                              foreground="black")
                toplevel.entries[4].configure(state='enabled', foreground="black")
            else:
                for i in range(1, 5):
                    toplevel.entries[i].configure(state='readonly', foreground=self.styleObj.colors.get('secondary'))
                for i in range(1, 4):
                    toplevel.entries[i].configure(value=[])
                toplevel.stringVar[1].set("TASK-000000-[A-Z]")
                toplevel.stringVar[2].set("Employee Name")
                toplevel.stringVar[3].set("Work Progress")
                toplevel.stringVar[4].set("2024-06-15")

        try:
            rowDetails = self.tableview.get_row(iid=self.tableview.view.focus()).values
            if rowDetails[-2] == "Output":
                popup.infoPopup(self, "Row selected is already located at Output.")
                return
        except:
            rowDetails = []
        updatables = self.db_connection.query_task_updatable()

        # Creates Popup
        toplevel = popup(master=self.masterWindow, title="Update Task", entryFieldQty=5)

        # Creates Widgets
        toplevel.create_title_frame(frame=toplevel.frameList[0], title="Update Task")
        for index, key in enumerate(
                ["Task ID", "Batch ID", "Assigned Employee", "Progress", "Estimated Time Of Completion"]):
            toplevel.create_label(frame=toplevel.frameList[index + 1], label=key)
            toplevel.create_errMsg(frame=toplevel.frameList[index + 1], errVar=toplevel.errVar[index])
        toplevel.create_combobox(frame=toplevel.frameList[1], stringVar=toplevel.stringVar[0],
                                 options=[value[0] for value in updatables])
        toplevel.create_combobox(frame=toplevel.frameList[2], stringVar=toplevel.stringVar[1], state='readonly')
        toplevel.create_combobox(frame=toplevel.frameList[3], stringVar=toplevel.stringVar[2], state="readonly")
        toplevel.create_combobox(frame=toplevel.frameList[4], stringVar=toplevel.stringVar[3], state='readonly')
        toplevel.create_dateEntry(frame=toplevel.frameList[5], stringVar=toplevel.stringVar[4], state="readonly")
        toplevel.create_buttonbox(frame=toplevel.frameList[6])
        toplevel.submitButton.configure(command=lambda: onSubmitButton())

        # Preview Text
        entryList = ["taskEntry", "taskBatchEntry", "employeeNameEntry", "progressEntry", "etaEntry"]
        for index, value in enumerate(entryList):
            previewText(toplevel.entries[index], key=value)

        # Validation
        valObj = validation()
        for index in [0, 1, 2, 3, 4]:
            valObj.validate(widget=toplevel.entries[index], key="string", errStringVar=toplevel.errVar[index])

        # Bindings
        toplevel.bind_entry_return()
        toplevel.traceButton()

        toplevel.stringVar[0].trace("w", onTaskEntry)

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
                ["Batch No", "Task 1", "Task 2", "Task 3", "Task 4", "Assigned Employee"]):
            toplevel.create_label(frame=toplevel.frameList[index + 1], label=key)
            toplevel.create_errMsg(frame=toplevel.frameList[index + 1], errVar=toplevel.errVar[index])
        toplevel.create_entry(frame=toplevel.frameList[1], stringVar=toplevel.stringVar[2])
        toplevel.create_combobox(frame=toplevel.frameList[2], stringVar=toplevel.stringVar[2],
                                 options=["Task A", "Task B"])
        toplevel.create_combobox(frame=toplevel.frameList[3], stringVar=toplevel.stringVar[3],
                                 options=["Task A", "Task B"])
        toplevel.create_combobox(frame=toplevel.frameList[4], stringVar=toplevel.stringVar[4],
                                 options=["Task A", "Task B"])
        toplevel.create_combobox(frame=toplevel.frameList[5], stringVar=toplevel.stringVar[5],
                                 options=["Task A", "Task B"])
        toplevel.create_buttonbox(frame=toplevel.frameList[6])

        # Preview Text
        entryList = ["taskDescriptionEntry", "taskDescriptionEntry", "taskDescriptionEntry", "taskDescriptionEntry",
                     "employeeNameEntry"]
        for index, value in enumerate(entryList):
            previewText(toplevel.entries[index], key=value)

        # Validation
        #valObj = validation()
        #for index in [0, 1, 2, 3, 4, 5]:
        #    valObj.validate(widget=toplevel.entries[index], key="string", errStringVar=toplevel.errVar[index])

        # Bindings
        toplevel.bind_entry_return()
        toplevel.traceButton()

        # Configure Frames
        for index in range(1, 6):
            toplevel.configure_frame(frame=toplevel.frameList[index])

        # Grid Frames
        toplevel.configure_toplevel()

    def deletePopup(self):
        rowDetails = popup.getTableRows(self.tableview)
        if rowDetails == []:
            return
        if popup.deleteDialog(self) == "OK":
            #print(rowDetails)
            if self.db_connection.delete_task(rowDetails[0]):
                self._load_table_rows(self.db_connection.query_task_table())
            else:
                popup.deleteFail(self)



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
    rFrame = taskFrame(window, "Administrator")
    lFrame = navigationFrame(window, 1, rFrame)

    #rFrame.createPopup()

    # Starts Event Main Loop
    window.mainloop()
