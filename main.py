import ttkbootstrap as ttk
from Frames import *
from Frames.inventoryFrame import inventoryFrame
from Database.Database import DatabaseConnection

def main():

    # Create Main Window, and center it
    window = ttk.Window(title="Keai IWMS", themename="flatly", size=(1280, 720))
    ttk.window.Window.place_window_center(window)

    # Creates Login Object
    def onLogin(loginInstance:ttk.Frame, email: str) -> None:
        loginInstance.destroy()
        #rFrame=inventoryFrame(window, "Administrator")
        db_connection = DatabaseConnection()
        employeeID = db_connection.query_employee_login(email)
        lFrame=navigationFrame(window, employeeID, ttk.Frame())
        lFrame.getButtonCommand("Dashboard")
        window.rowconfigure(0, weight=1)
        window.columnconfigure(0, weight=1, minsize=200)
        window.columnconfigure(1, weight=20)

    instance = Login(window, onLogin_callback=onLogin)
    # onLogin(instance, "ahmad@gmail.com")

    # Starts Event Main Loop
    window.mainloop()


if __name__ == "__main__":
    main()
