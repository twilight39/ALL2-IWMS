import ttkbootstrap as ttk
from PIL import Image, ImageTk

from utils import fonts
from configuration import Configuration

from Frames.notificationFrame import notificationFrame


class DashboardFrame(ttk.Frame):
    def __init__(self, master: ttk.window.Window, role: str):
        # Inherit ttk.Frame
        super().__init__(master)
        self.grid(row=0, column=1, sticky="nwes")

        # Create references
        self.masterWindow = master
        self.role = role
        self.styleObj = ttk.style.Style.get_instance()
        self.font = fonts()
        self.config = Configuration()
        graphics_path = self.config.getGraphicsPath()
        self.images = [
            Image.open(f'{graphics_path}/notificationIcon.png').resize((50, 50))
        ]
        self.imageObject = []
        for im in self.images:
            self.imageObject += [ImageTk.PhotoImage(image=im)]

        # Create Vertical Frames
        top_frame = ttk.Frame(self)
        top_frame.grid(row=1, column=1, sticky="nwes")

        middle_frame = ttk.Frame(self, bootstyle="light")
        middle_frame.grid(row=2, column=1, sticky="nwes")

        bottom_frame = ttk.Frame(self)
        bottom_frame.grid(row=3, column=1, sticky="nwes")

        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=4)
        self.rowconfigure(3, weight=16)
        self.columnconfigure(1, weight=1)

        # Top Frame Widgets
        dashboard_label = ttk.Label(top_frame, text="Dashboard", font=self.font.fonts["header3"])
        self.styleObj.configure(style="light.TButton", background="white", borderwidth=0)
        notificationButton = ttk.Button(top_frame, image=self.imageObject[0], bootstyle="light",
                                        command=lambda: notificationFrame(self.masterWindow, self.role))
        dashboard_label.grid(row=1, column=1, sticky="nw", padx=20, pady=20)
        notificationButton.grid(row=1, column=2, sticky="nes")

        top_frame.rowconfigure(1, weight=1)
        top_frame.rowconfigure(2, weight=3)
        top_frame.columnconfigure(1, weight=1)
        top_frame.columnconfigure(2, weight=0)

        # Middle Frame
        self.configure_middle_frame(middle_frame)

    def configure_middle_frame(self, middle_frame: ttk.Frame):
        # Create Frames
        left_frame = ttk.Frame(middle_frame, bootstyle="light", padding=10)
        left_frame.grid(row=1, column=1, sticky="nwes")

        right_frame = ttk.Frame(middle_frame, bootstyle="light")
        right_frame.grid(row=1, column=2, sticky="nwes")

        middle_frame.rowconfigure(1, weight=1)
        middle_frame.columnconfigure(1, weight=3)
        middle_frame.columnconfigure(2, weight=1)

        # Left Frame
        ttk.Label(left_frame, text="Sales Activity", font=self.font.get_font("regular4"), foreground="black",
                  bootstyle="inverse-light").grid(row=0, column=0, columnspan= 4, sticky="nw")
        self._info_frame(left_frame, column=0, info="Sales Order Created")
        self._info_frame(left_frame, column=1, info="Sales Order Pending")
        self._info_frame(left_frame, column=2, info="Sales Order Delivered")
        self._info_frame(left_frame, column=3, info="Stock Sold")

        left_frame.rowconfigure(0, weight=0)
        left_frame.rowconfigure(1, weight=1)
        left_frame.columnconfigure(0, weight=1)
        left_frame.columnconfigure(1, weight=1)
        left_frame.columnconfigure(2, weight=1)
        left_frame.columnconfigure(3, weight=1)

        # Right Frame
        ttk.Label(right_frame, text="Inventory Summary", font=self.font.get_font("regular4"), foreground="black",
                  bootstyle="inverse-light").grid(row=0, column=1, sticky="nw")

    def _info_frame(self, parent: ttk.Frame, column: int, info: str, query: callable = None):
        frame = ttk.Frame(parent, bootstyle="", padding=10, relief="raised", borderwidth=5)
        frame.grid(row=1, column=column, sticky="nwes", padx=5)

        # ttk.Label(frame, text=query())
        ttk.Label(frame, text=info, font=self.font.get_font("thin3"), foreground=self.styleObj.colors.get(
            "secondary"), anchor=ttk.CENTER).grid(row=3, column=0, sticky="nwe")

        frame.rowconfigure(3, weight=1)
        frame.columnconfigure(0, weight=1)



if __name__ == "__main__":
    from navigationFrame import navigationFrame

    # Create Main Window, and center it
    window = ttk.Window(title="Keai IWMS", themename="litera", size=(1280, 720))
    ttk.window.Window.place_window_center(window)
    window.rowconfigure(0, weight=1)
    window.columnconfigure(0, weight=1, minsize=200)
    window.columnconfigure(1, weight=20)

    # Creates Frames
    lFrame = navigationFrame(window, 1, ttk.Frame(window))
    lFrame.getButtonCommand("Dashboard")

    # Starts Event Main Loop
    window.mainloop()
