from abc import ABC, abstractmethod
from utils import *
import ttkbootstrap as ttk
from ttkbootstrap.tableview import Tableview
from  ttkbootstrap.toast import ToastNotification
from ttkbootstrap.dialogs import Messagebox
from PIL import Image, ImageTk
from functools import partial

from Frames.notificationFrame import notificationFrame
from configuration import Configuration

class pageFrame(ttk.Frame, ABC):

    def __init__(self, master: ttk.Window, title: str, button_config: dict, role: str) -> None:
        """
        Abstract base class of a page frame.

        Args:
            master (ttk.Window): Master window.
            title (str): Page header.
            button_config (dict): Key->["Worker", "Supervisor", "Administrator];
                                  Values should be a list of all valid buttons.
            role (str): Role of operator.
        """

        # Inherit ttk.Frame
        super().__init__(master)
        self.grid(row=0, column=1, sticky="nwes")

        # Create references
        self.masterWindow = master
        self.button_config = button_config
        self.role = role
        self.styleObj = ttk.style.Style.get_instance()
        self.font = fonts()
        self.config= Configuration()
        graphicsPath = self.config.getGraphicsPath()
        self.images = [
            Image.open(f'{graphicsPath}/notificationIcon.png').resize((50, 50))
            ]
        self.imageObject = []
        for im in self.images:
            self.imageObject += [ImageTk.PhotoImage(image=im)]

        # Create Frames
        topFrame = ttk.Frame(self)
        topFrame.grid(row=1, column=1, sticky="nwes")

        bottomFrame = ttk.Frame(self)
        bottomFrame.grid(row=2, column=1, sticky="nwes")

        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=20)
        self.columnconfigure(1, weight=1)

        # Top Frame Widgets
        productLabel = ttk.Label(topFrame, text=title, font=self.font.fonts["header3"])
        self.styleObj.configure(style="light.TButton", background="white", borderwidth=0)
        notificationButton = ttk.Button(topFrame, image=self.imageObject[0], bootstyle="light", command=lambda: notificationFrame(self.masterWindow, self.role))
        productLabel.grid(row=1, column=1, sticky="nw", padx=20, pady=20)
        notificationButton.grid(row=1, column=2, sticky="nes")

        buttonFrame = ttk.Frame(topFrame, padding=20)
        buttonFrame.grid(row=2, column=1, columnspan=2, sticky="nwes")
        self._create_buttons(buttonFrame)

        topFrame.rowconfigure(1, weight=1)
        topFrame.rowconfigure(2, weight=3)
        topFrame.columnconfigure(1, weight=1)
        topFrame.columnconfigure(2, weight=0)

        # Bottom Frame Widgets
        self.tableview = Tableview(
            master=bottomFrame,
            searchable=True,
            stripecolor=(self.styleObj.theme.colors.get("light"), None),
            autofit=True,
            bootstyle="primary"
        )
        self.tableview.grid(row=1, column=1, sticky="nwes")

        y_scrollbar = ttk.Scrollbar(bottomFrame, orient="vertical", command=self.tableview.winfo_children()[1].yview, bootstyle="secondary-round")
        y_scrollbar.grid(row=1, column=2, sticky="ns")

        bottomFrame.rowconfigure(1, weight=1)
        bottomFrame.columnconfigure(1, weight=1)

    def _create_buttons(self, buttonFrame:ttk.Frame) -> None:
        self.styleObj.configure(style="warning.TButton", font=self.font.get_font("regular2"), foreground="black")
        for col, button_text in enumerate(self.button_config.get(self.role, []), start=1):
            button = ttk.Button(buttonFrame, text=button_text, bootstyle="warning", command=lambda x=button_text: self.getButtonCommand(x))
            button.grid(row=1, column=col, sticky="nwes", padx=5)

        buttonFrame.rowconfigure(1, weight=1)
        if self.role == "Worker":
            buttonFrame.columnconfigure(0, weight=5)
        buttonFrame.columnconfigure(tuple(range(1, len(self.button_config.get(self.role, [])) + 1)), weight=1)

    @abstractmethod
    def _insert_table_headings(self, colNames:list) -> None:
        pass

    def _insert_table_columns(self, colName:str) -> None:
        self.tableview.insert_column(
            index="end",
            text=colName,
            anchor="center",
            stretch=True
        )
    def _load_table_rows(self, rowList:list) -> None:
        self.tableview.delete_rows()
        for list in rowList:
            self.tableview.insert_row('end', list)
        self.tableview.load_table_data()

    @abstractmethod
    def getButtonCommand(self, button_text):
        pass


class popup(ttk.window.Toplevel, ABC):

    def __init__(self, master: ttk.window.Window, title: str, entryFieldQty: int, **kwargs) -> None:

        # Inherit TopLevel widget
        super().__init__(title=title, transient=master, topmost=True, **kwargs)
        self.place_window_center()
        self.grab_set()

        # Font Object Reference
        self.font = fonts()

        # Initialise variables
        self.frameList = [ttk.Frame(self, padding=10) for _ in range(entryFieldQty+2)]
        self.frameList[0].configure(padding=0, bootstyle="warning")
        self.stringVar = [ttk.StringVar() for _ in range(entryFieldQty)]
        self.errVar = [ttk.StringVar() for _ in range(entryFieldQty + 1)]
        self.entries = []
        self.errLabels = []

        # Use public methods to place widgets in self.frameList
        # Call preview objects on self.entries
        # Bind validations to self.entries, then change self.errLabels

    def create_title_frame(self, frame: ttk.Frame, title: str) -> None:
        label = ttk.Label(frame, text=title, bootstyle="warning-inverse", foreground="black", anchor="center", font=self.font.get_font("header2"))
        label.grid(row=1, column=1, sticky="nwes")

        frame.rowconfigure(1, weight=1)
        frame.columnconfigure(1, weight=1)

    def create_label(self, frame: ttk.Frame, label: str) -> None:
        label = ttk.Label(frame, text=label)
        label.grid(row=0, column=1, sticky="sw")

    def create_entry(self, frame: ttk.Frame, stringVar: ttk.StringVar, state = "enabled") -> None:
        if state == "enabled":
            entry = ttk.Entry(master=frame, textvariable=stringVar, state="enabled")
        elif state == "readonly":
            entry = ttk.Entry(master=frame, textvariable=stringVar, state="readonly")
        else:
            print(f"Entry field created with invalid state \nFrame: {frame}\nState: {state}")
        #print(entry.cget("state"))
        entry.grid(row=1, column=1, sticky="we")
        self.entries += [entry]

    def create_dateEntry(self, frame: ttk.Frame, stringVar: ttk.StringVar, state = "enabled") -> None:
        if state == "enabled":
            entry = ttk.DateEntry(master=frame, dateformat=r"%Y-%m-%d",firstweekday=0)
            entry.entry.configure(textvariable=stringVar, state="enabled")
        elif state == "readonly":
            entry = ttk.DateEntry(master=frame, dateformat=r"%Y-%m-%d",firstweekday=0)
            entry.entry.configure(textvariable=stringVar, state="readonly")
        else:
            print(f"Entry field created with invalid state \nFrame: {frame}\nState: {state}")
        #print(entry.cget("state"))
        entry.grid(row=1, column=1, sticky="we")
        self.entries += [entry.entry]

    def create_spinbox(self, frame: ttk.Frame, stringVar: ttk.StringVar, state = "enabled", to=1000) -> None:
        if state == "enabled":
            entry = ttk.Spinbox(master=frame, textvariable=stringVar, state="enabled", increment=1, from_=0, to=to)
        elif state == "readonly":
            entry = ttk.Spinbox(master=frame, textvariable=stringVar, state="readonly", increment=1, from_=0, to=to)
        else:
            print(f"Spinbox field created with invalid state \nFrame: {frame}\nState: {state}")
        #print(entry.cget("state"))
        entry.grid(row=1, column=1, sticky="we")
        self.entries += [entry]

    def create_combobox(self, frame: ttk.Frame, stringVar: ttk.StringVar, options: list = [], state= "enabled", postcommand=None):
        if state == "enabled":
            #print(postcommand)
            entry = ttk.Combobox(master=frame, textvariable=stringVar, values=options, postcommand=postcommand)
        elif state == "readonly":
            entry = ttk.Combobox(master=frame, textvariable=stringVar, values=options, state="readonly", postcommand=postcommand)
        else:
            print(f"Combobox created with invalid state \nFrame: {frame}\nState: {state}")

        entry.grid(row=1, column=1, sticky="we")
        self.entries += [entry]

    def create_errMsg(self, frame: ttk.Frame, errVar: ttk.StringVar) -> None:
        errMsg = ttk.Label(master=frame, textvariable=errVar, foreground=ttk.style.Style.get_instance().theme.colors.get("danger"), font=self.font.get_font("error"))
        errMsg.grid(row=2, column=1, sticky="nwe")
        self.errLabels += [errMsg]

    def create_buttonbox(self, frame: ttk.Frame):
        #print(f"Function given: {command}")
        self.submitButton = ttk.Button(master=frame, text="Submit", bootstyle="success", state="disabled")
        self.submitButton.focus_set()
        self.submitButton.grid(row=1, column=2, sticky="e")

        cnl_btn = ttk.Button(master=frame, text="Cancel", command=lambda: self.destroy(), bootstyle="danger")
        cnl_btn.grid(row=1, column=1, sticky="e")

        errVar = ttk.StringVar()
        self.errVar += [errVar]
        errMsg = ttk.Label(master=frame, textvariable=errVar, foreground=ttk.style.Style.get_instance().theme.colors.get("danger"), font=self.font.get_font("error"))
        errMsg.grid(row=2, column=0, columnspan=3, sticky="ne")

        frame.rowconfigure(1, weight=1)
        frame.rowconfigure(2, weight=0)
        frame.columnconfigure(0, weight=20)
        frame.columnconfigure(1, weight=1)
        frame.columnconfigure(2, weight=1)

    @staticmethod
    def deleteDialog(parent:ttk.TTK_WIDGETS) -> str:
        """Returns: 'OK' or 'Cancel' """
        return Messagebox.okcancel(message="Action cannot be undone. Proceed to deletion?", title="Warning", parent=parent)

    @staticmethod
    def deleteFail(parent:ttk.TTK_WIDGETS) -> Messagebox.show_info:
        return Messagebox.show_info(title="Info", message="Operation failed. There are likely linked data entries in the existing database.", parent=parent)

    @staticmethod
    def infoPopup(parent:ttk.TTK_WIDGETS, msg:str) -> Messagebox.show_info:
        return Messagebox.show_info(title="Info", message=msg, parent=parent)

    @staticmethod
    def getTableRows(tableview:ttk.tableview) -> list:
        try:
            rowDetails = tableview.get_row(iid=tableview.view.focus()).values
            return rowDetails
        except:
            ToastNotification(
                title="Please select a table row",
                message="Please select the details you would you like to operate on.",
                duration=3000
            ).show_toast()
            return []

    # Enables submit button if all entry fields are not greyed out
    def validateButton(self):
        if validation.validateButton(self.submitButton, self.stringVar, self.entries):
            self.submitButton.configure(state="enabled")
        else:
            self.submitButton.configure(state="disabled")

    # Binds all entries to validateButon
    def traceButton(self):
        for entry in self.entries:
            #print(f"Entry Traced: {entry}")
            entry.bind("<FocusOut>", lambda event: self.validateButton(), add="+")
            entry.bind("<KeyRelease>", lambda event: self.validateButton(), add="+")
            entry.bind("<ButtonRelease>", lambda event: self.validateButton(), add="+")

    # Binds enter to the next entry field
    def bind_entry_return(self):
        next_index = 1
        for index in range(1, len(self.entries)):
            self.entries[index - 1].bind("<Return>",lambda event, x=next_index: self.entries[x].focus())
            next_index += 1
        self.entries[-1].bind("<Return>", lambda event: self.submitButton.focus())

    def configure_frame(self, frame):
        """Configure Entry Field frames only"""
        frame.rowconfigure(0, weight=1)
        frame.rowconfigure(1, weight=1)
        frame.rowconfigure(2, weight=1)
        frame.columnconfigure(1, weight=1)

    def configure_toplevel(self):
        for index, frame in enumerate(self.frameList, start=1):
            frame.grid(row=index, column=1, sticky="nwes")
            self.rowconfigure(index, weight=1)
        self.rowconfigure(len(self.frameList)+1, weight=1)
        self.columnconfigure(1, weight=1)