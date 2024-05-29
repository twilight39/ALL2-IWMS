import ttkbootstrap as ttk
from Frames import *
from Frames.productFrame import productFrame

def main():

    # Create Main Window, and center it
    window = ttk.Window(title="Keai IWMS", themename="flatly", size=(1280, 720))
    ttk.window.Window.place_window_center(window)

    # Creates Login Object
    def onLogin(loginInstance:ttk.Frame, employeeID:int):
        loginInstance.destroy()
        rFrame=productFrame(window, "Administrator")
        lFrame=navigationFrame(window, employeeID, rFrame)
        window.rowconfigure(0, weight=1)
        window.columnconfigure(0, weight=1, minsize=200)
        window.columnconfigure(1, weight=20)

    instance = Login(window, onLogin_callback=onLogin)
    onLogin(instance, 1)

    # Starts Event Main Loop
    window.mainloop()


if __name__ == "__main__":
    main()
