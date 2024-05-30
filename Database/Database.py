import sqlite3
import os
import bcrypt
import base64
import hashlib
from datetime import date, datetime

from configuration import Configuration

def singleton(cls):
    """Decorator to create a singleton class."""
    instances = {}
    def wrapper(*args, **kwargs):
        #print(f"wrapper started for {cls}")
        if cls not in instances:
            #print("no instance found")
            instances[cls] = cls(*args, **kwargs)
        #print(f"Returning this instance: {str(instances[cls])}" )
        return instances[cls]

    return wrapper

@singleton
class DatabaseConnection:

    def __init__(self):
        self.config = Configuration()
        db_filepath = self.config.getDatabaseFile()
        #print(f"DatabaseConnection Constructor-> Database File Path\n{db_filepath}")

        if not os.path.exists(db_filepath):
            self.connection = sqlite3.connect(db_filepath)
            self.cursor = self.connection.cursor()
            self._create_tables()
            self.connection.commit()

        else:
            self.connection = sqlite3.connect(db_filepath)
            self.cursor = self.connection.cursor()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.connection:
            self.connection.close()

    def query_employee(self, employeeID:int) -> tuple:
        """Returns: [EmployeeName: str, RoleName: str]"""
        self.cursor.execute("SELECT w.Name, r.RoleName FROM Roles r INNER JOIN Workers w ON w.RoleID = r.RoleID WHERE w.WorkerID = ?",
                            (employeeID, ))
        return self.cursor.fetchone()

    def query_notification(self, employeeID:int) -> list:
        try:
            self.cursor.execute("SELECT RoleID FROM Workers WHERE WorkerID = ?", (employeeID,))
            roleID = self.cursor.fetchone()[0]
            notifications = []

            for index in range(3, roleID-1, -1):
                self.cursor.execute("SELECT NotificationID, TimeStamp, NotificationDesc FROM Notification WHERE WorkerID = ?", (index,))
                notifications += self.cursor.fetchall()

            notifications = sorted(notifications, key = lambda timestamp:notifications[1])
            return notifications

        except sqlite3.Error as err:
            print(f"Error: {err}")
            return []

    def add_notification(self, employeeID:int, message:str) -> bool:
        try:
            self.cursor.execute("""INSERT INTO Notification (WorkerID, Timestamp, NotificationDesc)
                VALUES (?, ?, ?)""", (employeeID, datetime.now(), message,))
            self.connection.commit()
            return True

        except sqlite3.Error as err:
            print(f"Error: {err}")
            return False

    def delete_notifcation(self, notificationID:int) -> bool:
        try:
            self.cursor.execute("DELETE FROM Notification WHERE NotificationID = ?", (notificationID,))
            self.connection.commit()
            return True

        except sqlite3.Error as err:
            print(f"Error: {err}")
            return False

    def add_productBatch(self, batchnumber: str) -> bool:
        self.cursor.execute("INSERT INTO Product_Batch (PBatchNumber) VALUES (?)", (batchnumber,))

    def query_product(self) -> list:
        try:
            self.cursor.execute("SELECT ProductID, ProductName, Description FROM Products")
            products = self.cursor.fetchall()
            return products
        except sqlite3.Error:
            return []

    def add_product(self, product_name:str, description:str, price:float, preferred_supplier_id:int) -> bool:
        try:
            self.cursor.execute("""
                INSERT INTO Products (ProductName, Description, Price, PreferredSupplierID)
                VALUES (?, ?, ?, ?)
                """, (product_name, description, price, preferred_supplier_id))
            self.connection.commit()
            return True

        except sqlite3.Error as err:
            print(f"Error: {err}")
            return False

    def receive_product(self, productID: int, batchNumber: int, quantity: int) -> bool:
        try:
            #print("function called")
            self.cursor.execute("""
            INSERT INTO Inventory (ProductID, StockQuantity, LocationID, PBatchID)
            VALUES (?, ?, ?, ?)
            """, (productID, quantity, 1, batchNumber,))
            #print("no error")
            self.connection.commit()
            return True

        except sqlite3.Error as err:
            print(f"Error: {err}")
            return False

    def update_product(self, productID: int, batchNumber: int, srcLocationID: int, desLocationID: int, quantity:int) -> bool:
        try:
            srcQuantity = self.cursor.execute("""
                SELECT StockQuantity FROM Inventory WHERE ProductID = ? AND PBatchID = ? AND LocationID = ?
                """, (productID, batchNumber, srcLocationID,))
            srcQuantity = srcQuantity.fetchone()[0] - quantity

            self.cursor.execute("""
                UPDATE Inventory 
                SET StockQuantity = ?
                WHERE ProductID = ? AND PBatchID = ? AND LocationID = ?
                """, (srcQuantity, productID, batchNumber, srcLocationID,))

            desQuantity = self.cursor.execute("""
                                        SELECT StockQuantity FROM Inventory WHERE ProductID = ? AND PBatchID = ? AND LocationID = ?
                                        """, (productID, batchNumber, desLocationID,))
            try:
                desQuantity = desQuantity.fetchone()[0] + quantity

                self.cursor.execute("""
                    UPDATE Inventory 
                    SET StockQuantity = ?
                    WHERE ProductID = ? AND PBatchID = ? AND LocationID = ?
                    """, (desQuantity, productID, batchNumber, desLocationID,))
            except:
                desQuantity = quantity

                self.cursor.execute("""
                    INSERT INTO Inventory (ProductID, StockQuantity, LocationID, PBatchID)
                    VALUES (?, ?, ?, ?)
                    """, (productID, quantity, desLocationID, batchNumber,))

            self.connection.commit()

        except sqlite3.Error as err:
            print(f"Error: {err}")
            return False

    def delete_product(self, productID: int, batchID: int, locationID: int) -> bool:
        try:
            self.cursor.execute("DELETE FROM Inventory WHERE ProductID = ?, PBatchID = ?, LocationID =?",
                                (productID, batchID, locationID,))
            self.connection.commit()

        except sqlite3.Error as err:
            print(f"Error: {err}")
            return False

    def query_vendor(self) -> list:
        """Returns: [(VendorID: int, VendorName: str),]"""
        self.cursor.execute("SELECT SupplierID, Name FROM Suppliers")
        return self.cursor.fetchall()

    def add_vendor(self, name:str, contact_number:str, email:str) -> bool:
        try:
            self.cursor.execute("INSERT INTO Suppliers (Name, ContactNumber, Email) VALUES (?, ?, ?)",
                           (name, contact_number, email))
            self.connection.commit()
            return True

        except sqlite3.Error as err:
            print(f"Error: {err}")
            return False

    def edit_vendor(self,supplier_id:int, name:str, contact_number:str, email:str) -> bool:
        try:
            self.cursor.execute("UPDATE Suppliers SET Name = ?, ContactNumber = ?, Email = ? WHERE SupplierID = ?",
                           (name, contact_number, email, supplier_id))
            self.connection.commit()
            return True

        except sqlite3.Error as err:
            print(f"Error: {err}")
            return False

    def delete_vendor(self, supplier_id: int) -> bool:
        try:
            self.cursor.execute("DELETE FROM Suppliers WHERE SupplierID = ?", (supplier_id,))
            self.connection.commit()
            return True

        except sqlite3.Error as err:
            print(f"Error: {err}")
            return False

    def query_tasks(self) -> list:
        self.cursor.execute("""
            SELECT TaskID, Workers.Name, TaskDesc, TaskStatus, ETA
            FROM Tasks
            INNER JOIN Workers ON Tasks.WorkerID = Workers.WorkerID
        """)
        return self.cursor.fetchall()

    def add_task(self, description: str, eta: str, worker_id: int = None, batch_id: int = None) -> bool:
        try:
            self.cursor.execute("""
                INSERT INTO Tasks (TaskDesc, WorkerID, ETA, TaskStatus, TBatchID)
                VALUES (?, ?, ?, 'Not Started', ?)
            """, (description, worker_id, eta, batch_id))
            self.connection.commit()
            return True

        except sqlite3.Error as err:
            print(f"Error: {err}")
            return False

    def update_task(self, task_id:int, description:str, worker_id:int, progress:str, eta:str, batch_id: int = None) -> bool:
        try:
            self.cursor.execute("""
                UPDATE Tasks
                SET TaskDesc = ?, WorkerID = ?, TaskStatus = ?, ETA = ?, TBatchID =?
                WHERE TaskID = ?
            """, (description, worker_id, progress, eta, batch_id,task_id))
            self.connection.commit()
            return True

        except sqlite3.Error as err:
            print(f"Error: {err}")
            return False

    def delete_task(self, task_id:int) -> bool:
        try:
            self.cursor.execute("DELETE FROM Tasks WHERE TaskID = ?", (task_id,))
            self.connection.commit()
            return True

        except sqlite3.Error as err:
            print(f"Error: {err}")
            return False

    def query_taskBatch(self) -> list:
        try:
            self.cursor.execute("SELECT TBatchID, TBatchDesc FROM Task_Batch")
            return self.cursor.fetchall()
        except sqlite3.Error:
            return []

    def add_taskBatch(self, batchDesc:str, taskIDs: list) -> bool:
        try:
            self.cursor.execute("INSERT INTO Task_Batch (TBatchDesc) VALUES (?)", (batchDesc,))
            self.cursor.execute("SELECT TBatchID FROM Task_Batch WHERE TBatchDesc = ?", (batchDesc, ))
            batchID = self.cursor.fetchone()[0]
            for i in taskIDs:
                self.cursor.execute("""
                UPDATE Tasks
                SET TBatchID = ?
                WHERE TaskID = ?
                """, (batchID, i,))
            self.connection.commit()
            return True
        except sqlite3.Error as err:
            print(f"Error: {err}")
            return False

    def update_taskBatch(self, batchID: int, batchDesc:str = "", taskIDs: list = [], employeeID:int = 0) -> bool:
        try:
            if batchDesc != "":
                self.cursor.execute("UPDATE Task_Batch SET TBatchDesc = ? WHERE TBatchID = ?", (batchDesc, batchID,))

            if taskIDs:
                self.cursor.execute("UPDATE Tasks SET TBatchID = NULL WHERE TBatchID = ?", (batchID,))
                for index in taskIDs:
                    self.cursor.execute("UPDATE Tasks SET TBatchID = ? WHERE TaskID = ?", (batchID, index))

            if employeeID != 0:
                self.cursor.execute("UPDATE Tasks SET WorkerID = ? WHERE TBatchID =?", (employeeID, batchID))

            self.connection.commit()
            return True

        except sqlite3.Error as err:
            print(f"Error: {err}")
            return False

    def delete_taskBatch(self, batchID: int) -> bool:
        try:
            self.cursor.execute("""UPDATE Tasks SET TBatchID = NULL WHERE TBatchID = ?""", (batchID,))
            self.cursor.execute("""DELETE FROM Task_Batch WHERE TBatchID = ?""", (batchID,))
            self.connection.commit()
            return True

        except sqlite3.Error as err:
            print(f"Error: {err}")
            return False

    def query_purchaseOrder(self):
        """Returns: [Purchase ID: int, Product Name: str, Quantity: int, Batch Number: int, Vendor Name: str, Date: str]"""
        try:
            self.cursor.execute("""
            SELECT s.ShipmentID, p.ProductName, s.Quantity, s.PBatchID, v.Name, s.ShipmentDate
            FROM Shipments s 
            LEFT JOIN Products p ON s.ProductID = p.ProductID
            LEFT JOIN Suppliers v ON s.SupplierID = v.SupplierID
            """)
            return self.cursor.fetchall()

        except sqlite3.Error as err:
            print(f"Error: {err}")
            return False

    def add_purchaseOrder(self, productID:int, quantity:int, vendorID:int, batchID:int) -> bool:
        try:
            self.cursor.execute("""INSERT INTO Shipments (ProductID, Quantity, SupplierID, ShipmentDate, PBatchID)
            VALUES (?, ?, ?, ?, ?)""", (productID, quantity, vendorID, date.today(), batchID,))
            self.connection.commit()
            return True

        except sqlite3.Error as err:
            print(f"Error: {err}")
            return False

    def delete_purchaseOrder(self, purchaseOrderID: int) -> bool:
        try:
            self.cursor.execute("DELETE FROM Shipments WHERE ShipmentID = ?", (purchaseOrderID,))
            return True

        except sqlite3.Error as err:
            print(f"Error: {err}")
            return  False

    def query_salesOrder(self) -> list:
        """Returns: [Sales ID, Product Name, Quantity, Batch ID, Date]"""
        try:
            self.cursor.execute("""
            SELECT s.SaleID, p.ProductName, i.QuantitySold, i.PBatchID, s.Date
            FROM Sales s
            LEFT JOIN Sales_Inventory i ON s.SaleID = i.SaleID
            LEFT JOIN Products p ON i.ProductID = p.ProductID
            """)
            return self.cursor.fetchall()

        except sqlite3.Error as err:
            print(f"Error: {err}")
            return []

    def add_salesOrder(self, productID: int, batchID: int, quantity: int) -> bool:
        try:
            self.cursor.execute("INSERT INTO Sales (Date) VALUES (?)", (date.today(),))
            saleID = self.cursor.lastrowid
            # Query Price from Product Table
            self.cursor.execute("SELECT Price FROM Products WHERE ProductID = ?", (productID,))
            unitPrice = self.cursor.fetchone()[0]
            self.cursor.execute("INSERT INTO Sales_Inventory (SaleID, ProductID, PBatchID, QuantitySold, UnitPrice) VALUES (?, ?, ?, ?, ?)", (saleID, productID, batchID, quantity, unitPrice))
            self.connection.commit()
            return True

        except sqlite3.Error as err:
            print(f"Error: {err}")
            return False

    def update_salesOrder(self, saleID: int, productID:int, batchID:int, quantity:int) -> bool:
        """Adds another product into a Sales Order."""
        try:
            self.cursor.execute("SELECT Price FROM Products WHERE ProductID = ?", (productID,))
            unitPrice = self.cursor.fetchone()[0]
            self.cursor.execute("""INSERT INTO Sales_Inventory (SaleID, ProductID, PBatchID, QuantitySold, UnitPrice)
                                        VALUES (?, ?, ?, ?, ?)""",
                                        (saleID, productID, batchID, quantity, unitPrice))
            self.connection.commit()
            return True

        except sqlite3.Error as err:
            print(f"Error: {err}")
            return False

    def delete_salesOrder(self, saleID:int) -> bool:
        try:
            self.cursor.execute("DELETE FROM Sales_Inventory WHERE SaleID = ?", (saleID,))
            self.cursor.execute("DELETE FROM Sales WHERE SaleID = ?", (saleID,))
            self.connection.commit()
            return  True

        except sqlite3.Error as err:
            print(f"Error: {err}")
            return False

    def _create_tables(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS Roles (
            RoleID INTEGER PRIMARY KEY AUTOINCREMENT,
            RoleName TEXT(64) NOT NULL);
            ''')

        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS Workers (
            WorkerID INTEGER PRIMARY KEY AUTOINCREMENT,
            RoleID INTEGER NOT NULL,
            Name TEXT NOT NULL,
            ContactNumber TEXT(12),
            FOREIGN KEY (RoleID) REFERENCES Roles(RoleID));
            ''')

        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS Accounts (
            WorkerID INTEGER PRIMARY KEY,
            Email TEXT UNIQUE NOT NULL,
            HashedPW TEXT(72) NOT NULL,
            FOREIGN KEY (WorkerID) REFERENCES Workers(WorkerID));
            ''')

        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS Task_Batch (
            TBatchID INTEGER PRIMARY KEY AUTOINCREMENT,
            TBatchDesc TEXT);
            ''')

        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS Tasks (
            TaskID INTEGER PRIMARY KEY AUTOINCREMENT,
            WorkerID INTEGER,
            TaskDesc TEXT,
            TaskStatus TEXT,
            ETA TEXT,
            TBatchID INTEGER,
            FOREIGN KEY (TBatchID) REFERENCES Task_Batch(TBatchID),
            FOREIGN KEY (WorkerID) REFERENCES Workers(WorkerID));
            ''')

        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS Notification (
            NotificationID INTEGER PRIMARY KEY AUTOINCREMENT,
            WorkerID INTEGER NOT NULL,
            TimeStamp TEXT,
            NotificationDesc TEXT,
            FOREIGN KEY (WorkerID) REFERENCES Workers(WorkerID));
            ''')

        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS Product_Batch (
            PBatchID INTEGER PRIMARY KEY AUTOINCREMENT,
            PBatchNumber TEXT);
            ''')

        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS Suppliers (
            SupplierID INTEGER PRIMARY KEY AUTOINCREMENT,
            Name TEXT NOT NULL,
            Email TEXT,
            ContactNumber TEXT(12));
            ''')

        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS Locations (
            LocationID INTEGER PRIMARY KEY AUTOINCREMENT,
            LocationName TEXT(64) NOT NULL);
            ''')

        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS Products (
            ProductID INTEGER PRIMARY KEY AUTOINCREMENT,
            ProductName TEXT NOT NULL,
            Description TEXT,
            Price REAL,
            PreferredSupplierID INTEGER NOT NULL,
            FOREIGN KEY (PreferredSupplierID) REFERENCES Suppliers(SupplierID));
            ''')

        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS Inventory (
            InventoryID INTEGER PRIMARY KEY AUTOINCREMENT,
            ProductID INTEGER NOT NULL,
            StockQuantity INTEGER,
            LocationID INTEGER,
            PBatchID INTEGER,
            FOREIGN KEY (PBatchID) REFERENCES Product_Batch(PBatchID),
            FOREIGN KEY (ProductID) REFERENCES Products(ProductID),
            FOREIGN KEY (LocationID) REFERENCES Locations(LocationID));
            ''')

        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS Shipments (
            ShipmentID INTEGER PRIMARY KEY AUTOINCREMENT,
            ProductID INTEGER NOT NULL,
            Quantity INTEGER NOT NULL,
            SupplierID INTEGER NOT NULL,
            ShipmentDate TEXT NOT NULL,
            PBatchID TEXT NOT NULL,
            FOREIGN KEY (ProductID) REFERENCES Products(ProductID),
            FOREIGN KEY (PBatchID) REFERENCES Product_Batch(PBatchID),
            FOREIGN KEY (SupplierID) REFERENCES Suppliers(SupplierID));
            ''')

        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS Sales (
            SaleID INTEGER PRIMARY KEY AUTOINCREMENT,
            Date TEXT);
            ''')

        self.cursor.execute('''
            CREATE TABLE Sales_Inventory (
            SalesInventoryID INTEGER PRIMARY KEY AUTOINCREMENT,
            SaleID INTEGER NOT NULL,
            ProductID INTEGER NOT NULL,
            PBatchID INTEGER NOT NULL,
            QuantitySold INTEGER,
            UnitPrice REAL,
            FOREIGN KEY (PBatchID) REFERENCES Product_Batch(PBatchID),
            FOREIGN KEY (SaleID) REFERENCES Sales(SaleID),
            FOREIGN KEY (ProductID) REFERENCES Products(ProductID));
            ''')

        self.cursor.execute("INSERT INTO Roles (RoleName) VALUES ('Administrator');")
        self.cursor.execute("INSERT INTO Roles (RoleName) VALUES ('Supervisor');")
        self.cursor.execute("INSERT INTO Roles (RoleName) VALUES ('Worker');")

        self.cursor.execute("INSERT INTO Locations (LocationName) VALUES ('Input');")
        self.cursor.execute("INSERT INTO Locations (LocationName) VALUES ('Warehouse');")
        self.cursor.execute("INSERT INTO Locations (LocationName) VALUES ('Packing Zone');")
        self.cursor.execute("INSERT INTO Locations (LocationName) VALUES ('Output');")

        self.cursor.execute("INSERT INTO Workers (RoleID, Name, ContactNumber) VALUES (1, 'Ahmad', '0161123344');")
        self.cursor.execute("INSERT INTO Accounts (WorkerID, Email, HashedPW) VALUES (1, 'ahmad@gmail.com', ?)", (b'$2b$14$OQM2OwY9kdaOeA/IE0hhPeXwrQhbZwVxxJvlynbkRDfXB1dm6XSOy',))

@singleton
class authentication:

    def __init__(self):
        self.db_connection = DatabaseConnection()
        #print(f"Authentication Constructor -> DatabaseConnection reference\n{self.db_connection}")
        pass

    def authenticate(self, email:str, password:str) -> bool:
        cursor = self.db_connection.cursor
        cursor.execute("SELECT HashedPW FROM Accounts WHERE Email = ?", (email,))
        try:
            hashed = cursor.fetchone()[0]
        except:
            return False
        if bcrypt.checkpw(base64.b64encode(hashlib.sha256(password.encode()).digest()), hashed):
            return True
        return False

    def resetPassword(self, employeeID:int, password:str) -> None:
        cursor = self.db_connection.cursor
        hashed = bcrypt.hashpw(base64.b64encode(hashlib.sha256(password.encode()).digest()), bcrypt.gensalt(rounds=14))
        try:
            cursor.execute("""UPDATE Accounts SET HashedPW = ? WHERE WorkerID = ?""", (hashed, employeeID,))
            self.db_connection.connection.commit()
        except sqlite3.Error as err:
            print(f"Error: {err}")

    def createAccount(self, adminID:int , adminPassword: str, employeeEmail: str, employeeRoleID: int, employeeName: str, employeeContactNumber: str ,employeePassword: str) -> bool:
        cursor = self.db_connection.cursor

        # Checks if Admin is creating the account
        cursor.execute("SELECT RoleID FROM Workers WHERE WorkerID = ?", (adminID,))
        if cursor.fetchone()[0] != 1:
            print("not admin")
            return False

        # Authenticate Admin
        cursor.execute("SELECT Email FROM Accounts WHERE WorkerID = ?", (adminID,))
        if self.authenticate(cursor.fetchone()[0], adminPassword):
            hashed = bcrypt.hashpw(base64.b64encode(hashlib.sha256(employeePassword.encode()).digest()), bcrypt.gensalt(rounds=14))

            # Insert Account
            try:
                cursor.execute("""INSERT INTO Workers (RoleID, Name, ContactNumber) VALUES (?, ?, ?)""", (employeeRoleID, employeeName, employeeContactNumber,))
                employeeID = cursor.lastrowid
                cursor.execute("INSERT INTO Accounts (WorkerID, Email, HashedPW) VALUES (?, ?, ?)", (employeeID, employeeEmail, hashed,))
                self.db_connection.connection.commit()
                return True

            except sqlite3.Error as e:
                print(f"Error:{e}")
                return False

        print("admin failed to authenticate.")
        return False


    def deleteAccount(self, adminID:int, password:str, employeeID:int) -> bool:
        cursor = self.db_connection.cursor

        # Checks if Admin is creating the account
        cursor.execute("SELECT RoleID FROM Workers WHERE WorkerID = ?", (adminID,))
        if cursor.fetchone()[0] != 1:
            print("not admin")
            return False

        # Authenticate Admin
        cursor.execute("SELECT Email FROM Accounts WHERE WorkerID = ?", (adminID,))
        if self.authenticate(cursor.fetchone()[0], password):
            try:
                cursor.execute("DELETE FROM Accounts WHERE WorkerID = ?", (employeeID,))
            except sqlite3.Error as err:
                print(f"Error: {err}")
                return False
        return False

# Test Case
if __name__ == "__main__":
    print(datetime.now())
    #auth = authentication()
    #if auth.authenticate("ahmad@gmail.com", "admin1234"):
    #    print("true")

    #if auth.authenticate("john@example.com", "JohnIsDumb"):
    #    print ("true")

    """
    auth.createAccount(
        adminID=1,
        adminPassword="admin1234",
        employeeEmail="john@example.com",
        employeeName="John Doe",
        employeeRoleID=2,
        employeeContactNumber="123-456-7890",
        employeePassword="JohnIsDumb"
    )
    """
    #auth.createAccount(

    #)

    #con = DatabaseConnection()
    #con.add_salesOrder()