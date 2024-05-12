import tkinter
import ttkbootstrap as ttk
from PIL import ImageTk, Image
from utils import previewText

class Login(ttk.Frame):

    def __init__(self, master):
        # Application Images
        self.images =[
            Image.open('Graphics/loginBG.png').resize((1280, 720))
        ]

        self.imageObject = []
        for im in self.images:
            self.imageObject += [ImageTk.PhotoImage(image=im)]

        # Entry Widget Values
        self.textVariables ={
            "email" : tkinter.StringVar(),
            "emailError" : tkinter.StringVar(),
            "password" : tkinter.StringVar(),
            "passwordError" : tkinter.StringVar()
        }

        # Style Object Reference
        self.styleObj = master.style

        # Inherit Frame Class
        super().__init__(master)

        # Grid Master Window
        master.rowconfigure(0, weight=1)
        master.columnconfigure(0, weight=1)

        # Grid Self Frame
        self.grid(column=0, row=0, sticky="nwes")
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        # Background Image
        canvas = tkinter.Canvas(self)
        canvas.grid(row=0, column=0, sticky="nwes")
        canvas.create_image(0, 0, anchor="nw", image=self.imageObject[0])

        # Binding to resize image, currently window not resizable
        # canvas.bind('<Configure>', lambda event, imageNo=0: self.on_resize(event, imageNo))

        '''
        # Create frame over canvas
        frame = ttk.Frame(self)
        canvas.create_window(0, 0, window=frame)
        frame.rowconfigure(0, weight=1)
        frame.columnconfigure(0, weight=1)
        '''

        # Text Labels
        canvas.create_text(40, 100, text="KEAI", font=("Noto Sans", 55, "bold"), fill="black", anchor=tkinter.W)
        canvas.create_text(40, 160, text="Warehouse and Inventory Management System", font=("Noto Sans", 45, "bold"), fill="black", anchor=tkinter.W)
        emailText = canvas.create_text(255, 330, text="Email", font=("Noto Sans", 38, "bold"), fill="black", anchor=tkinter.E)
        passwordText = canvas.create_text(255, 390, text="Password", font=("Noto Sans", 38, "bold"), fill="black", anchor=tkinter.E)

        # Login Button
        fnt = tkinter.font.Font(family='Noto Sans', name='appButtonFont', size=38, weight='bold')
        self.styleObj.configure(style="warning.TButton", font = fnt, foreground="black")
        loginButton = ttk.Button(self, text="Login", style="warning")

        # Debugging Button aaaAaaaAaaaAaaa
        # print(master.style)
        # print(master.style.theme_names())
        print(loginButton['style'])
        print(loginButton.winfo_class())
        # print(master.style.theme.colors.get("danger"))

        # Email & Password Widgets
        errFont = tkinter.font.Font(family="Lexend", name="appErrorTextFont", size=11, slant="italic")
        greyColor = self.styleObj.theme.colors.get("secondary")
        errColor = self.styleObj.theme.colors.get("danger")

        emailEntry = ttk.Entry(self, textvariable=self.textVariables["email"], font=('Noto Sans', 18),foreground=greyColor)
        emailError = ttk.Label(self, textvariable=self.textVariables["emailError"], font=errFont, foreground=errColor)
        passwordEntry = ttk.Entry(self, textvariable=self.textVariables["password"], font=('Noto Sans', 18), foreground=greyColor, show ="*")
        passwordError = ttk.Label(self, textvariable=self.textVariables["passwordError"], font=errFont, foreground=errColor)

        # Preview Text
        previewText(emailEntry, "emailEntry", self.styleObj)
        previewText(passwordEntry, "passwordEntry", self.styleObj)

        # Add Widgets to Canvas
        emailEntryID = canvas.create_window(290, 307, window=emailEntry, width= 350, height=46, anchor=tkinter.NW)
        passwordEntryID = canvas.create_window(290, 367, window=passwordEntry, width=350, height=46, anchor=tkinter.NW)
        canvas.create_window(360, 500, window=loginButton)

        # Debugging
        print("Email Label (x1, y1, x2, y2): " + str(canvas.bbox(emailText)))
        print("Email Entry (x1, y1, x2, y2): " + str(canvas.bbox(emailEntryID)))
        print("Password Label (x1, y1, x2, y2): " + str(canvas.bbox(passwordText)))
        print("Password Entry (x1, y1, x2, y2): " + str(canvas.bbox(passwordEntryID)))

    """
    # Resize Images to Window Size, Currently Window not resizable
    def on_resize(self, event, imageNo):

        # Get current window size
        window_width = self.winfo_width()
        window_height = self.winfo_height()

        # Update image size
        resizedImage = self.images[imageNo].resize((window_width, window_height))
        self.imageObject[imageNo] = ImageTk.PhotoImage(resizedImage)
        # event.widget.configure(image=self.imageObject[imageNo])
        event.widget.create_image(0, 0, anchor="nw", image = self.imageObject[imageNo])

        # Debugging
        # print("WindowL: W" + str(window_width) + " H" + str(window_height))
        # print("Widget: W" + str(event.widget.winfo_width()) + " H" +str(event.widget.winfo_height()))
    """

# Test case

if __name__ == "__main__":
    # Create Main Window, and center it
    window = ttk.Window(title="Keai IWMS", themename="journal", size=(1280, 720), resizable=[False,False])
    ttk.window.Window.place_window_center(window)

    # Creates Login Object
    instance = Login(window)

    # Starts Event Main Loop
    window.mainloop()

    pass