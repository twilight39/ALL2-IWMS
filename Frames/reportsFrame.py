import ttkbootstrap as ttk

from Frames.pageFrame import pageFrame
from Database import DatabaseConnection


class ReportFrame(pageFrame):
    def __init__(self, master: ttk.window.Window, role: str, employee_id: int):
        # Inherits Page Frame
        super().__init__(master=master,
                         title="Reports",
                         role=role,
                         button_config={
                             "Worker": ["Product Movement", "Stock Level"],
                             "Supervisor": ["Product Movement", "Stock Level", "Performance Report", "Traceability Report"],
                             "Administrator": ["Product Movement", "Stock Level", "Performance Report",
                                               "Traceability Report", "User Activities"]
                         },
                         employeeID=employee_id)

        self.db_connection = DatabaseConnection()

        self.product_movement_report()

    def product_movement_report(self):
        self.tableview.grid()
        column_names = ("Date", "Product", "Batch No.", "From", "To", "Quantity", "Status")
        self._insert_table_headings(column_names)
        self._load_table_rows(self.db_connection.query_product_movement_report())

    def stock_level_report(self):
        self.tableview.grid()
        column_names = ("Product", "Unit Cost", "Total Value", "On Hand", "Free to Use", "Incoming", "Outgoing")
        self._insert_table_headings(column_names)
        self._load_table_rows(self.db_connection.query_stock_level_report())

    def performance_report(self):
        ttk.Toplevel(master=self.master, width=400, height= 150, resizable=(False, False))

    def _insert_table_headings(self, column_names: tuple) -> None:
        self.tableview.purge_table_data()
        # print(column_names)

        for column in column_names:
            self._insert_table_columns(column)

    def getButtonCommand(self, button_text):
        if button_text == "Product Movement":
            self.product_movement_report()

        elif button_text == "Stock Level":
            self.stock_level_report()

        elif button_text == "Performance Report":
            self.performance_report()



if __name__ == '__main__':
    from navigationFrame import navigationFrame

    # Create Main Window, and center it
    window = ttk.Window(title="Keai IWMS", themename="litera", size=(1280, 720))
    ttk.window.Window.place_window_center(window)
    window.rowconfigure(0, weight=1)
    window.columnconfigure(0, weight=1, minsize=200)
    window.columnconfigure(1, weight=20)

    # Creates Frames
    lFrame = navigationFrame(window, 1, ttk.Frame(window))
    lFrame.getButtonCommand("Report")

    # Starts Event Main Loop
    window.mainloop()
