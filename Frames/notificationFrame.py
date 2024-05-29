import ttkbootstrap as ttk
from ttkbootstrap.scrolled import ScrolledFrame
from PIL import ImageTk, Image
from utils import fonts
from configuration import Configuration

class notificationFrame(ttk.Frame):

    def __init__(self, master: ttk.Window, role: str) -> None:

        self.master = master
        self.Fonts = fonts()
        self.config = Configuration()
        graphicsPath = self.config.getGraphicsPath()
        self.icon = Image.open(f'{graphicsPath}/notificationIcon.png').resize((40, 40))
        self.icon = ImageTk.PhotoImage(image=self.icon)

        # Creates and places Notification Frame
        super().__init__(master, bootstyle="secondary")
        self.placeNotificationFrame()
        master.bind("<Configure>", lambda event: self.placeNotificationFrame(), add="+")

        # Create Widgets
        topFrame = ttk.Frame(self, bootstyle="warning")
        bottomFrame = ScrolledFrame(self, bootstyle="secondary-round")
        bottomFrame.configure(bootstyle="light")
        lSeparator = ttk.Separator(self, bootstyle="dark", orient="vertical")

        notification = ttk.Label(topFrame, bootstyle="inverse-warning", text="Notifications", anchor="center", font=self.Fonts.get_font("regular"), foreground="black")
        notificationButton = ttk.Button(topFrame, image=self.icon, bootstyle="warning", command=lambda: self.destroy())
        bSeparator = ttk.Separator(topFrame, bootstyle="dark")

        #for x in range(50):
        #    ttk.Checkbutton(bottomFrame, text=f"Checkbutton {x}").pack(anchor=ttk.W)


        # Grid Frames
        topFrame.grid(row=0, column=1, sticky="nwes")
        bottomFrame.grid(row=1, column=1, sticky="nwes")
        lSeparator.grid(row=0, column=0, rowspan=2, sticky="nws")

        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=10)
        self.columnconfigure(0, weight=0)
        self.columnconfigure(1, weight=1)

        # Top Frame Widgets
        notification.grid(row=0, column=0, sticky="nwes")
        notificationButton.grid(row=0, column=1, sticky="nwes")
        bSeparator.grid(row=1, column=0, columnspan=2, sticky="wes")

        topFrame.rowconfigure(0, weight=1)
        topFrame.rowconfigure(1, weight=0)
        topFrame.columnconfigure(0, weight=1)
        topFrame.columnconfigure(1, weight=1)

        # Bottom Frame Widgets
        for i in range(20):
            ttk.Label(bottomFrame, text="Label " + str(i+1), font=self.Fonts.get_font("header3"), anchor="center").grid(row=i, column=1, sticky="nwes")
            bottomFrame.rowconfigure(i, weight=1)
        #bottomFrame.columnconfigure(0, weight=0)
        bottomFrame.columnconfigure(1, weight=1)

    def placeNotificationFrame(self):
        #print("Place called")
        width = 0.2*self.master.winfo_width()
        height = self.master.winfo_height()
        #print("W"+ str(width) + " H" + str(height))
        try:
            self.place(relx=0.8, rely=0, width=width, height=height)
        except:
            pass


if __name__ == "__main__":
    from navigationFrame import navigationFrame

    # Create Main Window, and center it
    window = ttk.Window(title="Keai IWMS", themename="litera", size=(1280, 720))
    ttk.window.Window.place_window_center(window)
    window.rowconfigure(0, weight=1)
    window.columnconfigure(0, weight=1, minsize=200)
    window.columnconfigure(1, weight=20)

    # Creates Frames
    lFrame = navigationFrame(window, "Administrator")
    notifs = notificationFrame(window, "Administrator")
    window.mainloop()