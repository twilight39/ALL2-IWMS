import tkinter
import ttkbootstrap as ttk
from PIL import ImageTk, Image
from utils import previewText, validation

class Login(tkinter.Canvas):

    def __init__(self, master):

        self.master = master

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
            "passwordError" : tkinter.StringVar(),
        }

        # Style Object Reference
        self.styleObj = master.style

        # Validation Object
        self.validationObj = validation()

        # Inherit Frame Class
        super().__init__(master)

        # Pack Canvas
        self.pack(fill="both", expand=True)

        # Background Image
        self.create_image(0, 0, anchor="nw", image=self.imageObject[0])

        # Binding to resize image, currently window not resizable
        # self.bind('<Configure>', lambda event, imageNo=0: self.on_resize(event, imageNo))

        # Text Labels
        self.create_text(40, 100, text="KEAI", font=("Noto Sans", 55, "bold"), fill="black", anchor=tkinter.W)
        self.create_text(40, 160, text="Warehouse and Inventory Management System", font=("Noto Sans", 45, "bold"), fill="black", anchor=tkinter.W)
        emailText = self.create_text(255, 330, text="Email", font=("Noto Sans", 38, "bold"), fill="black", anchor=tkinter.E)
        passwordText = self.create_text(255, 400, text="Password", font=("Noto Sans", 38, "bold"), fill="black", anchor=tkinter.E)

        # Login Button
        fnt = tkinter.font.Font(family='Noto Sans', name='appButtonFont', size=38, weight='bold')
        self.styleObj.configure(style="warning.TButton", font = fnt, foreground="black")
        loginButton = ttk.Button(self, text="Login", style="warning")

        # Debugging Button aaaAaaaAaaaAaaa
        # print(master.style)
        # print(master.style.theme_names())
        print(loginButton['style'])
        # print(loginButton.winfo_class())
        # print(master.style.theme.colors.get("danger"))

        # Email & Password Widgets
        errFont = tkinter.font.Font(family="Lexend", name="appErrorTextFont", size=11, slant="italic")
        greyColor = self.styleObj.theme.colors.get("secondary")
        errColor = self.styleObj.theme.colors.get("danger")

        emailEntry = ttk.Entry(self, textvariable=self.textVariables["email"], font=('Noto Sans', 18),foreground=greyColor, bootstyle="dark")
        passwordEntry = ttk.Entry(self, textvariable=self.textVariables["password"], font=('Noto Sans', 18), foreground=greyColor, show ="*", bootstyle="dark")

        # Preview Text
        previewText(emailEntry, "emailEntry", self.styleObj)
        previewText(passwordEntry, "passwordEntry", self.styleObj)

        # Add Widgets to Canvas
        emailEntryID = self.create_window(290, 307, window=emailEntry, width= 350, height=46, anchor=tkinter.NW)
        emailErrorID = self.create_text(290, 353, font=errFont, fill=errColor, anchor=tkinter.NW)
        passwordEntryID = self.create_window(290, 377, window=passwordEntry, width=350, height=46, anchor=tkinter.NW)
        passwordErrorID = self.create_text(290, 423, font=errFont, fill=errColor, anchor=tkinter.NW)
        loginButtonID = self.create_window(360, 500, window=loginButton)
        buttonErrorID = self.create_text(360, 530, font=errFont, fill=errColor, anchor=tkinter.N)#, text="Invalid Email or Password")

        # Visual Validation
        self.VisualValidation(emailEntry, "email", self.textVariables["emailError"], emailErrorID)
        self.VisualValidation(passwordEntry, "password", self.textVariables["passwordError"], passwordErrorID)

        # Debugging
        print("Email Label (x1, y1, x2, y2): " + str(self.bbox(emailText)))
        print("Email Entry (x1, y1, x2, y2): " + str(self.bbox(emailEntryID)))
        print("Password Label (x1, y1, x2, y2): " + str(self.bbox(passwordText)))
        print("Password Entry (x1, y1, x2, y2): " + str(self.bbox(passwordEntryID)))
        print("Login Button (x1, y1, x2, y2): " + str(self.bbox(loginButtonID)))


        # Validate Login Button
        loginButton.bind("<ButtonPress-1>", lambda event, x=buttonErrorID:self.ValidateButton(event, x))

        # Bind Enter Key
        # Email Entry -> Password Entry -> Login Button

    # Validates a widget and updates its error message
    def VisualValidation(self, widget, key, errStringVar, errID):
        self.validationObj.validate(widget, key, errStringVar)
        widget.bind("<FocusOut>", lambda event: self.itemconfigure(errID, text=errStringVar.get()), add="+")

    # Temporary Check if Login succeeds; Replace once database is implemented!!!
    def ValidateButton(self, event, buttonErrorID):
        if (self.textVariables["email"].get() != "abc@companyKEAI.com" and
            self.textVariables["emailError"].get() == "" and
            self.textVariables["password"].get() != "abcd1234!" and
            self.textVariables["passwordError"].get() == ""
        ):
            self.itemconfigure(buttonErrorID, text="")

        else:
            self.itemconfigure(buttonErrorID, text="Invalid Email or Password")


# Test case

if __name__ == "__main__":
    # Create Main Window, and center it
    window = ttk.Window(title="Keai IWMS", themename="cosmo", size=(1280, 720), resizable=[False,False])
    ttk.window.Window.place_window_center(window)

    # Creates Login Object
    instance = Login(window)

    # Starts Event Main Loop
    window.mainloop()

    pass