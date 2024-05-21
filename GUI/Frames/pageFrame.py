from abc import ABC, abstractmethod
from utils import *
import ttkbootstrap as ttk
from ttkbootstrap.tableview import Tableview
import ttkbootstrap.window

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
        productLabel.grid(row=1, column=1, sticky="nw", padx=20, pady=20)

        buttonFrame = ttk.Frame(topFrame, padding=20)
        buttonFrame.grid(row=2, column=1, sticky="nwes")
        self._create_buttons(buttonFrame)

        topFrame.rowconfigure(1, weight=1)
        topFrame.rowconfigure(2, weight=3)
        topFrame.columnconfigure(1, weight=1)

        # Bottom Frame Widgets
        self.tableview = Tableview(
            master=bottomFrame,
            searchable=True,
            autofit=True,
            stripecolor=(self.styleObj.theme.colors.get("light"), None),
            bootstyle="secondary"
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
        self.errVar = [ttk.StringVar() for _ in range(entryFieldQty)]
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

    def create_entry(self, frame: ttk.Frame, stringVar: ttk.StringVar) -> None:
        entry = ttk.Entry(master=frame, textvariable=stringVar)
        entry.grid(row=1, column=1, sticky="we")
        self.entries += [entry]

    def create_combobox(self, frame: ttk.Frame, stringVar: ttk.StringVar, options: list):
        entry = ttk.Combobox(master=frame, textvariable=stringVar, values=options)
        entry.grid(row=1, column=1, sticky="we")
        self.entries += [entry]

    def create_errMsg(self, frame: ttk.Frame, errVar: ttk.StringVar) -> None:
        errMsg = ttk.Label(master=frame, textvariable=errVar, foreground=ttk.style.Style.get_instance().theme.colors.get("danger"), font=self.font.get_font("error"))
        errMsg.grid(row=2, column=1, sticky="nwe")
        self.errLabels += [errMsg]

    def create_buttonbox(self, frame: ttk.Frame, command):
        self.submitButton = ttk.Button(master=frame, text="Submit", command=lambda: command, bootstyle="success", state="disabled")
        self.submitButton.focus_set()
        self.submitButton.grid(row=1, column=2, sticky="e")

        cnl_btn = ttk.Button(master=frame, text="Cancel", command=lambda: self.destroy(), bootstyle="danger")
        cnl_btn.grid(row=1, column=1, sticky="e")

        frame.rowconfigure(1, weight=1)
        frame.columnconfigure(0, weight=20)
        frame.columnconfigure(1, weight=1)
        frame.columnconfigure(2, weight=1)

    def validateButton(self, key):
        if validation.validateButton(self.submitButton, key, self.stringVar):
            self.submitButton.configure(state="enabled")
        else:
            self.submitButton.configure(state="disabled")

    def traceButton(self, key: list):
        for var in self.stringVar:
            var.trace("w", lambda x, y, z: self.validateButton(key))

    def bind_entry_return(self):
        next_index = 1
        for index in range(1, len(self.entries)):
            self.entries[index - 1].bind("<Return>",lambda event, x=next_index: self.entries[x].focus())
            next_index += 1
        self.entries[-1].bind("<Return>", lambda event: self.submitButton.focus())

    def configure_frame(self, frame):
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
