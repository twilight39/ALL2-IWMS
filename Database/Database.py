import sqlite3
import os
import bcrypt
import base64
import hashlib

from configuration import Configuration

def singleton(cls):
  """Decorator to create a singleton class."""
  instances = {}

  def wrapper(*args, **kwargs):
    if cls not in instances:
      instances[cls] = cls(*args, **kwargs)
    return instances[cls]

  return wrapper

@singleton
class DatabaseConnection:

    def __init__(self):
        self.config = Configuration()
        db_filepath = self.config.getDatabaseFile()
        print(db_filepath)

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

    def get_employee(self, employeeID:int) -> tuple:
        self.cursor.execute("SELECT w.Name, r.RoleName FROM Roles r INNER JOIN Workers w ON w.RoleID = r.RoleID WHERE w.WorkerID = ?",
                            (employeeID, ))
        return self.cursor.fetchone()
    def get_connection(self):
        return self.connection

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
            WorkerID INTEGER NOT NULL,
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
            PBatchDesc TEXT);
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
            FOREIGN KEY (ProductID) REFERENCES Products(ProductID),
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
        pass

    def authenticate(self, email:str, password:str) -> bool:
        connection = self.db_connection.get_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT HashedPW FROM Accounts WHERE Email = ?", (email,))
        try:
            hashed = cursor.fetchone()[0]
        except:
            return False
        if bcrypt.checkpw(base64.b64encode(hashlib.sha256(password.encode()).digest()), hashed):
            return True
        return False

    def resetPassword(self, employeeID:int, password:str) -> None:
        hashed = bcrypt.hashpw(base64.b64encode(hashlib.sha256(password.encode()).digest()), bcrypt.gensalt(rounds=14))
        # Store Hashed Password
        # Use EmployeeID unique key to update Accounts Table row

    def createAccount(self, adminID:int, employeeID: int, adminPassword: str, employeePassword: str) -> bool:
        # Retrieve Stored Hash from Database
        # Update once database implemented!!
        adminHashed = bcrypt.hashpw(base64.b64encode(hashlib.sha256(adminPassword.encode()).digest()), bcrypt.gensalt(rounds=14))
        if bcrypt.checkpw(base64.b64encode(hashlib.sha256(adminPassword.encode()).digest()), adminHashed):
            hashed = bcrypt.hashpw(base64.b64encode(hashlib.sha256(employeePassword.encode()).digest()), bcrypt.gensalt(rounds=14))
            # Use EmployeeID unique key to create Accounts Table row and store hash
            return True
        return False

    def deleteAccount(self, adminID:int, password:str, employeeID:int) -> bool:
        # Retrieve Stored Hash from Database
        # Update once database implemented!!
        adminHashed = bcrypt.hashpw(base64.b64encode(hashlib.sha256(password.encode()).digest()), bcrypt.gensalt(rounds=14))
        if bcrypt.checkpw(base64.b64encode(hashlib.sha256(password.encode()).digest()), adminHashed):
            # use employeeID unique key to delete Accounts Table row
            return True
        return False

# Test Case
if __name__ == "__main__":
    auth = authentication()
    auth.authenticate("ahmad@gmail.com", "admin1234")
    #print("b'$2b$14$OQM2OwY9kdaOeA/IE0hhPeXwrQhbZwVxxJvlynbkRDfXB1dm6XSOy'".decode("utf-8"))

    con = DatabaseConnection()
    con.get_role(1)