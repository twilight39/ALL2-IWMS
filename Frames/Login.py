import tkinter
import ttkbootstrap as ttk
from PIL import ImageTk, Image
from utils import previewText, validation, fonts
from Database import Database
from configuration import Configuration

class Login(tkinter.Canvas):

    def __init__(self, master:ttk.window, onLogin_callback=None):

        self.master = master
        self.state = True
        self.prevWindowDimensions =(1280, 720)

        config = Configuration()
        graphicsPath = config.getGraphicsPath()

        # Application Images
        self.images =[
            Image.open(f'{graphicsPath}/loginBG.png').resize((1280, 720)),
            Image.open(f'{graphicsPath}/passwordInvisible.png').resize(((24, 24))),
            Image.open(f'{graphicsPath}/passwordVisible.png').resize((32, 32))
        ]

        self.imageObject = []
        for im in self.images:
            self.imageObject += [ImageTk.PhotoImage(image=im)]

        # Entry Widget Values
        self.textVariables ={
            "email" : tkinter.StringVar(),
            "emailError" : tkinter.StringVar(),
            "password" : tkinter.StringVar(),
            "passwordError" : tkinter.StringVar(),
        }

        # References
        self.styleObj = master.style
        self.auth = Database.authentication()
        self.onLogin_callback = onLogin_callback

        # Validation & Fonts Object & Colors
        self.validationObj = validation()
        self.Fonts = fonts()
        greyColor = self.styleObj.theme.colors.get("secondary")
        errColor = self.styleObj.theme.colors.get("danger")

        # Inherit Frame Class
        super().__init__(master)
        self.grid(row=0, column=0, sticky="nwes")
        self.master.rowconfigure(0, weight=1)
        self.master.columnconfigure(0, weight=1)

        # Email & Password Widgets
        emailEntry = ttk.Entry(self, textvariable=self.textVariables["email"], font=self.Fonts.get_font("regular"),foreground=greyColor, bootstyle="dark")
        passwordEntry = ttk.Entry(self, textvariable=self.textVariables["password"], font=self.Fonts.get_font("regular"), foreground=greyColor, show ="*", bootstyle="dark")
        self.styleObj.configure(style="light.TButton", background="white", borderwidth=0)
        passwordButton = ttk.Button(self, image=self.imageObject[1], bootstyle="light", padding=0)
        passwordButton.configure(command=lambda: self.passwordVisible(passwordButton, passwordEntry))

        # Login Button Widget
        self.styleObj.configure(style="warning.TButton", font=self.Fonts.get_font("header3"), foreground="black")
        loginButton = ttk.Button(self, text="Login", style="warning", command=lambda: self.onLogin())

        # Bind Enter Key (Email Entry -> Password Entry -> Login Button)
        emailEntry.bind("<Return>", lambda event: passwordEntry.focus())
        passwordEntry.bind("<Return>", lambda event: loginButton.focus())

        # Preview Text
        previewText(emailEntry, "emailEntry")
        previewText(passwordEntry, "passwordEntry")

        # Display Canvas Objects
        self.canvasObjIDs = {
            "backgroundImageID": self.create_image(0, 0, anchor="nw", image=self.imageObject[0]),
            "KEAI": self.create_text(40, 100, text="KEAI", font=self.Fonts.get_font("header1"), fill="black",
                                     anchor=tkinter.W),
            "IWMS": self.create_text(40, 160, text="Warehouse and Inventory Management System",
                                     font=self.Fonts.get_font("header2"), fill="black", anchor=tkinter.W),
            "emailLabelID": self.create_text(270, 330, text="Email", font=self.Fonts.get_font("header3"), fill="black",
                                          anchor=tkinter.E),
            "emailEntryID" : self.create_window(290, 307, window=emailEntry, width=350, height=46, anchor=tkinter.NW),
            "emailErrorID" : self.create_text(290, 353, font=self.Fonts.get_font("error"), fill=errColor, anchor=tkinter.NW),
            "passwordLabelID": self.create_text(270, 400, text="Password", font=self.Fonts.get_font("header3"), fill="black", anchor=tkinter.E),
            "passwordEntryID" : self.create_window(290, 400, window=passwordEntry, width=350, height=46, anchor=tkinter.NW),
            "passwordButtonID" : self.create_window(638, 421, window=passwordButton, width=42, height=42, anchor=tkinter.NE),
            "passwordErrorID" : self.create_text(290, 423, font=self.Fonts.get_font("error"), fill=errColor, anchor=tkinter.NW),
            "loginButtonID" : self.create_window(360, 500, window=loginButton),
            "buttonErrorID" : self.create_text(360, 530, font=self.Fonts.get_font("error"), fill=errColor, anchor=tkinter.N)
        }
        for i in [2,3,4,6,7,10,11,12]:
            self.addtag_withtag("scalable", i)

        # Visual Validation
        self.VisualValidation(emailEntry, "email", self.textVariables["emailError"], self.canvasObjIDs["emailErrorID"])
        self.VisualValidation(passwordEntry, "password", self.textVariables["passwordError"], self.canvasObjIDs["passwordErrorID"])

        # Resize canvas with window
        self.bind("<Configure>", lambda event, x=passwordButton: self.DisplayCanvasObjects(event, x))

    def onLogin(self):
        print(self.textVariables["email"].get())
        print(self.textVariables["password"].get())
        if self.auth.authenticate(self.textVariables["email"].get(), self.textVariables["password"].get()):
            print("success")
            self.onLogin_callback(self, 1)
        else:
            self.itemconfigure(self.canvasObjIDs["buttonErrorID"], text="Invalid Email or Password")
            print("fail")

    def DisplayCanvasObjects(self, event, passwordButton):

        # Get new window size
        window_width = self.master.winfo_width()
        window_height = self.master.winfo_height()

        # Resize images
        self.resizeImages((window_width,window_height))

        # Redisplay Canvas Objects
        self.itemconfig(self.canvasObjIDs["backgroundImageID"], image=self.imageObject[0])
        self.scale("scalable", 0, 0, window_width/self.prevWindowDimensions[0], window_height/self.prevWindowDimensions[1])
        #self.itemconfig(self.canvasObjIDs["emailEntryID"], x=window_width/4.414, y=window_height/2.345)

        emailLabelDimensions = self.bbox(self.canvasObjIDs["emailLabelID"])
        passwordLabelDimensions = self.bbox(self.canvasObjIDs["passwordLabelID"])
        passwordButtonDimensions = self.bbox(self.canvasObjIDs["passwordLabelID"])[3] - self.bbox(self.canvasObjIDs["passwordLabelID"])[1] -4

        self.coords(self.canvasObjIDs["emailEntryID"], window_width/4.414, emailLabelDimensions[1])
        self.itemconfig(self.canvasObjIDs["emailEntryID"], width=window_width/2 - window_width/4.414, height=emailLabelDimensions[3]-emailLabelDimensions[1])
        self.coords(self.canvasObjIDs["passwordEntryID"], window_width/4.414, passwordLabelDimensions[1])
        self.itemconfig(self.canvasObjIDs["passwordEntryID"], width=window_width/2 - window_width/4.414, height=passwordLabelDimensions[3]-passwordLabelDimensions[1])

        self.coords(self.canvasObjIDs["passwordButtonID"], window_width/2 - 2, passwordLabelDimensions[1] + 2)
        self.itemconfig(self.canvasObjIDs["passwordButtonID"], width=passwordButtonDimensions, height=passwordButtonDimensions)

        if self.state == True:
            passwordButton.configure(image=self.imageObject[1])
        else:
            passwordButton.configure(image=self.imageObject[2])

        # Save current window size
        self.prevWindowDimensions = (window_width, window_height)

        # Debugging
        #print("Email Label (x1, y1, x2, y2): " + str(self.bbox(4)))
        #print("Email Entry (x1, y1, x2, y2): " + str(self.bbox(5)))
        #print("Password Label (x1, y1, x2, y2): " + str(self.bbox(7)))
        #print("Password Entry (x1, y1, x2, y2): " + str(self.bbox(8)))
        #print("Password Button (x1, y1, x2, y2): " + str(self.bbox(9)))
        #print("\n")

    # Validates a widget and updates its error message
    def VisualValidation(self, widget, key, errStringVar, errID):
        self.validationObj.validate(widget, key, errStringVar)
        widget.bind("<FocusOut>", lambda event: self.itemconfigure(errID, text=errStringVar.get()), add="+")

    def passwordVisible(self, button, entry):
        button.configure(image=self.imageObject[2], command=lambda: self.passwordInvisible(button, entry))
        entry.configure(show="")
        self.state = False

    def passwordInvisible(self, button, entry):
        button.configure(image=self.imageObject[1], command=lambda: self.passwordVisible(button, entry))
        entry.configure(show="*")
        self.state = True

    def resizeImages(self, dimensions: tuple):

        passwordButtonDimensions = self.bbox(self.canvasObjIDs["passwordLabelID"])[3] - self.bbox(self.canvasObjIDs["passwordLabelID"])[1]
        passwordButtonDimensions = (int(passwordButtonDimensions/1.917), int(passwordButtonDimensions/1.917))

        # Resize images
        resizedImages = [self.images[0].resize(dimensions),
                        self.images[1].resize(passwordButtonDimensions),
                        self.images[2].resize(tuple(int(x*1.5) for x in passwordButtonDimensions))]

        for id, im in enumerate(resizedImages):
            self.imageObject[id] = ImageTk.PhotoImage(image=im)


# Test case

if __name__ == "__main__":
    # Create Main Window, and center it
    window = ttk.Window(title="Keai IWMS", themename="flatly", size=(1280, 720), resizable=[True,True])
    ttk.window.Window.place_window_center(window)

    # Creates Login Object
    instance = Login(window)

    # Starts Event Main Loop
    window.mainloop()
