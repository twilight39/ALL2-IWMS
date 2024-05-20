import tkinter
import ttkbootstrap as ttk
from PIL import ImageTk, Image, ImageDraw
from utils import fonts

class navigationFrame(ttk.Frame):

    def __init__(self, master):

        # Button Configuration for roles
        buttonConfig = {
            "Worker" : ["Dashboard", "Product", "Report"],
            "Supervisor" : ["Dashboard", "Product", "Purchase Order", "Sales Order", "Tasks", "Vendor", "Report"],
            "Administrator": ["Dashboard", "Product", "Purchase Order", "Sales Order", "Tasks", "Vendor", "Report"]
        }

        # Inherit ttk.Frame, sets colour to warning
        super().__init__(master, bootstyle="warning")
        self.grid(row=0, column=0, sticky="nwes")

        # Application Images
        self.images = [
            Image.open('Graphics/settingsIcon.png').resize((40, 40)),
            self.make_circular_image('Graphics/testPFP.png', 200)
        ]

        self.imageObject = []
        for im in self.images:
            self.imageObject += [ImageTk.PhotoImage(image=im)]

        # References
        self.Fonts = fonts()
        self.styleObj = master.style
        self.role = "Administrator" # Database Logic Required

        # Create Widgets
        northFrame = ttk.Frame(self, bootstyle="warning", padding=20)
        southFrame = ttk.Frame(self, bootstyle="warning", padding=20)

        KEAILabel = ttk.Label(northFrame, text="KEAI", font=self.Fonts.fonts["header3"], bootstyle="warning-inverse", foreground="black")
        settingsIcon = ttk.Button(northFrame, image=self.imageObject[0],  bootstyle="warning")
        profilePicture = ttk.Label(northFrame, image=self.imageObject[1], bootstyle="warning-inverse") # Placeholder for user image
        userFrame = ttk.Frame(northFrame, bootstyle="warning")
        userName = ttk.Label(userFrame, text= "A Wild Kaiju", font=self.Fonts.fonts["regular2"], bootstyle="warning-inverse", foreground="black", anchor=tkinter.CENTER) # To query database
        userID = ttk.Label(userFrame, text="[Worker ID]", font=self.Fonts.fonts["regular2"], bootstyle="warning-inverse", foreground="black", anchor=tkinter.CENTER) # To query database

        # Grid Frames
        northFrame.grid(row=0, column=0, sticky="nwes")
        southFrame.grid(row=1, column=0, sticky="nwes")

        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=10)
        self.columnconfigure(0, weight=1)

        # Grid North Frame
        KEAILabel.grid(row=1, column=1, sticky="nw")
        settingsIcon.grid(row=1, column=3, sticky="ne")
        profilePicture.grid(row=2, column=1, sticky="nws")
        userFrame.grid(row=2, column=2, columnspan=2, sticky="nwes")

        northFrame.rowconfigure(1, weight=1)
        northFrame.rowconfigure(2, weight=2)
        northFrame.columnconfigure(1, weight=1)
        northFrame.columnconfigure(2, weight=2)
        northFrame.columnconfigure(3, weight=1)

        # Grid User Frame
        userName.grid(row=1, column=1, sticky="swe")
        userID.grid(row=2, column=1, sticky="nwe")

        userFrame.rowconfigure(1, weight=1)
        userFrame.rowconfigure(2, weight=1)
        userFrame.columnconfigure(1, weight=1)

        # Create and grid buttons
        self.styleObj.configure(style="dark.Link.TButton", font=self.Fonts.get_font("regular2"), foreground="black")
        for row, button_text in enumerate(buttonConfig[self.role], start=1):
            button = ttk.Button(southFrame, text=button_text, bootstyle="dark-link")
            button.grid(row=row, column=1, sticky="we")
            southFrame.rowconfigure(row, weight=1)
        southFrame.rowconfigure(0, weight=1)
        southFrame.columnconfigure(1, weight=1)

        if self.role == "Worker":
            southFrame.rowconfigure(4, weight=10)
        else:
            southFrame.rowconfigure(8, weight=1)



        # Debugging
        # self.bind("<Configure>", lambda event: print(self.winfo_width()))
        # print(dashboardButton['style'])
        #print(settingsIcon["style"])
        #self.configure(relief="sunken")
        #northFrame.configure(relief="sunken")
        #southFrame.configure(relief="sunken")
        #userFrame.configure(relief="sunken")
        #KEAILabel.configure(relief="sunken")

    def make_circular_image(self, image_path, output_diameter):

        img = Image.open(image_path).resize((output_diameter, output_diameter))

        mask = Image.new('L', (output_diameter, output_diameter), 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((0, 0, output_diameter, output_diameter), fill=255)

        output_img = Image.new(img.mode, (output_diameter, output_diameter), 0)
        output_img.paste(img, mask=mask)

        radius = int(output_diameter / 2)
        output_img = output_img.resize((radius, radius))

        return output_img



# Test Case
if __name__ == "__main__":

    # Create Main Window, and center it
    window = ttk.Window(title="Keai IWMS", themename="litera", size=(1280, 720))
    ttk.window.Window.place_window_center(window)
    window.rowconfigure(0, weight=1)
    window.columnconfigure(0, weight=1, minsize=200)
    window.columnconfigure(1, weight=20)

    # Creates Navigation Frame
    lFrame = navigationFrame(window)

    # Starts Event Main Loop
    window.mainloop()