import sqlite3
from datetime import datetime

# Connect to the database
conn = sqlite3.connect('TESTER ALL.db')
cursor = conn.cursor()

# Query Product (OK, but need to remove print for display instead)
def query_products():
    cursor.execute("SELECT ProductID, ProductName, Description FROM Products")
    products = cursor.fetchall()
    for product in products:
        print(f"ProductID: {product[0]}, ProductName: {product[1]}, Description: {product[2]}")

# Add Product (OK but the order of the details will change depending on the UI)
def insert_product(product_name, description, price, preferred_supplier_id):
        cursor.execute("""
            INSERT INTO Products (ProductName, Description, Price, PreferredSupplierID)
            VALUES (?, ?, ?, ?)
        """, (product_name, description, price, preferred_supplier_id))
        conn.commit()

# Delete product (Half OK)
def Delete_Product(product_id, pbatch_id, location_id, quantity_to_delete):
    # Query current quantity and product name
    cursor.execute("""
        SELECT i.StockQuantity, p.ProductName
        FROM Inventory i
        INNER JOIN Products p ON i.ProductID = p.ProductID
        WHERE i.ProductID = ? AND i.PBatchID = ? AND i.LocationID = ?
    """, (product_id, pbatch_id, location_id))
    result = cursor.fetchone()

    if result:
        current_quantity, product_name = result
        print(f"Current StockQuantity for {product_name}: {current_quantity}")
    else:
        print(f"No stock found for ProductID {product_id}, BatchID {pbatch_id}, LocationID {location_id}")
        return

    new_quantity = current_quantity - quantity_to_delete

    if new_quantity < 0:
        print(f"Error: Attempt to delete more quantity ({quantity_to_delete}) than available ({current_quantity}).")
        return

    # Update inventory
    cursor.execute("""
        UPDATE Inventory 
        SET StockQuantity = ? 
        WHERE ProductID = ? AND PBatchID = ? AND LocationID = ?
    """, (new_quantity, product_id, pbatch_id, location_id))

    conn.commit()
    print(f"Inventory updated. New StockQuantity for {product_name}: {new_quantity}")

    #I put if statement here to make have it as a backup aneh
    if new_quantity == 0:
        print(f"{product_name} stock quantity is zero.")

#Query Sales Order
def query_sales_order():
    # Query sales orders
    cursor.execute("""
        SELECT p.ProductName, si.QuantitySold, si.PBatchID, s.Date
        FROM Sales s
        JOIN Sales_Inventory si ON s.SaleID = si.SaleID
        JOIN Products p ON si.ProductID = p.ProductID
    """)
    sales_orders = cursor.fetchall()

    # Print results
    print("Sales Orders:")
    for order in sales_orders:
        product_name, quantity_sold, Pbatch_ID, date = order
        print(
            f"Product: {product_name}, Quantity: {quantity_sold}, Batch Number ID: {Pbatch_ID}, Date: {date}")

#Create Sales order (STUCK)
def create_sales_order(product_id, conn):
    try:
        cursor = conn.cursor()

        # Auto-generate current date
        current_date = datetime.now().strftime('%Y-%m-%d')

        # Query PBatchID via Product ID where Quantity >= 0
        cursor.execute("""
            SELECT PBatchID 
            FROM Inventory 
            WHERE ProductID = ? AND StockQuantity >= 0
        """, (product_id,))
        pbatch_ids = cursor.fetchall()

        # If no PBatchID found, exit
        if not pbatch_ids:
            print("No available stock for the specified product.")
            return

        # Choose the first available PBatchID
        pbatch_id = pbatch_ids[0][0]

        # Query quantity via PBatchID
        cursor.execute("SELECT StockQuantity FROM Sales_Inventory WHERE PBatchID = ?", (pbatch_id,))
        quantity = cursor.fetchone()[0]

        # Insert into Sales table
        cursor.execute("INSERT INTO Sales (Date) VALUES (?, ?)", (current_date))
        sale_id = cursor.lastrowid

        # Insert into Sales_Inventory table
        cursor.execute("""
            INSERT INTO Sales_Inventory (SaleID, ProductID, PBatchID, QuantitySold) 
            VALUES (?, ?, ?, ?)
        """, (sale_id, product_id, pbatch_id, quantity))

        conn.commit()
        print("Sales order created successfully.")
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")

#delete sales order (OK)
def delete_sales_order(sale_id, conn):
    try:
        cursor = conn.cursor()

        # Delete row from Sales_Inventory table
        cursor.execute("DELETE FROM Sales_Inventory WHERE SaleID = ?", (sale_id,))

        # Delete row from Sales table
        cursor.execute("DELETE FROM Sales WHERE SaleID = ?", (sale_id,))

        conn.commit()
        print("Sales order deleted successfully.")
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")

#Add Vendor (OK)
def add_vendor(name, contact_number, email, conn):
    try:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO Suppliers (Name, ContactNumber, Email) VALUES (?, ?, ?)", (name, contact_number, email))
        conn.commit()
        print("Vendor added successfully.")
    except sqlite3.Error as e:
        print(f"Error adding vendor: {e}")

# EDIT VENDOR (OK)
def edit_vendor(supplier_id, name, contact_number, email, conn):
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT SupplierID, Name FROM Suppliers")
        vendors = cursor.fetchall()
        cursor.execute("UPDATE Suppliers SET Name = ?, ContactNumber = ?, Email = ? WHERE SupplierID = ?", (name, contact_number, email, supplier_id))
        conn.commit()
        print("Vendor edited successfully.")
    except sqlite3.Error as e:
        print(f"Error editing vendor: {e}")

# Delete Vendor (OK)
def delete_vendor(supplier_id, conn):
    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Suppliers WHERE SupplierID = ?", (supplier_id,))
        conn.commit()
        print("Vendor deleted successfully.")
    except sqlite3.Error as e:
        print(f"Error deleting vendor: {e}")

# Task Query (OK)
def query_tasks():
    cursor.execute("""
        SELECT TaskID, Workers.Name, TaskDesc, TaskStatus, ETA
        FROM Tasks
        JOIN Workers ON Tasks.WorkerID = Workers.WorkerID
    """)
    tasks = cursor.fetchall()
    for task in tasks:
        print(task)

# Create Task (OK)
def create_task(description, worker_id, eta, batch_id):
    cursor.execute("""
        INSERT INTO Tasks (TaskDesc, WorkerID, ETA, TaskStatus, TBatchID)
        VALUES (?, ?, ?, 'Not Started', ?)
    """, (description, worker_id, eta, batch_id))
    conn.commit()

# Update Task (OK)
def update_task(task_id, description, worker_id, progress, eta):
    cursor.execute("""
        UPDATE Tasks
        SET TaskDesc = ?, WorkerID = ?, TaskStatus = ?, ETA = ?
        WHERE TaskID = ?
    """, (description, worker_id, progress, eta, task_id))
    conn.commit()

#Delete Task (OK)
def delete_task(task_id):
    # Delete the task from the Tasks table
    cursor.execute("DELETE FROM Tasks WHERE TaskID = ?", (task_id,))
    conn.commit()

#query for users (OK)
def query_users(conn):
    try:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT Workers.WorkerID, Workers.Name, Roles.RoleName, Accounts.Email, Workers.ContactNumber
            FROM Workers
            INNER JOIN Roles ON Workers.RoleID = Roles.RoleID
            INNER JOIN Accounts ON Workers.WorkerID = Accounts.WorkerID
        """)
        users = cursor.fetchall()
        for user in users:
            print(f"Employee ID: {user[0]}, Name: {user[1]}, Role: {user[2]}, Email: {user[3]}, Contact Number: {user[4]}")
    except sqlite3.Error as e:
        print(f"Error querying users: {e}")

# Add User (OK)
def add_user(name, role_id, email, contact_number, salt, hashed_pw, conn):
    try:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO Workers (Name, RoleID, ContactNumber) VALUES (?, ?, ?)
        """, (name, role_id, contact_number))
        worker_id = cursor.lastrowid

        cursor.execute("""
            INSERT INTO Accounts (WorkerID, Email, HashedPW, Salt) VALUES (?, ?, ?, ?)
        """, (worker_id, email, hashed_pw, salt))

        conn.commit()
        print("User added successfully.")
    except sqlite3.Error as e:
        print(f"Error adding user: {e}")


# Edit User (OK)
def edit_user(worker_id, name, role_id, email, contact_number, conn):
    try:
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE Workers 
            SET Name = ?, RoleID = ?, ContactNumber = ?
            WHERE WorkerID = ?
        """, (name, role_id, contact_number, worker_id))

        cursor.execute("""
            UPDATE Accounts 
            SET Email = ?
            WHERE WorkerID = ?
        """, (email, worker_id))

        conn.commit()
        print("User edited successfully.")
    except sqlite3.Error as e:
        print(f"Error editing user: {e}")

# Delete User(OK)
def delete_user(worker_id, conn):
    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Workers WHERE WorkerID = ?", (worker_id,))
        cursor.execute("DELETE FROM Accounts WHERE WorkerID = ?", (worker_id,))
        conn.commit()
        print("User deleted successfully.")
    except sqlite3.Error as e:
        print(f"Error deleting user: {e}")


def create_table():
    # Connect or create database (if it doesn't exist)
    conn = sqlite3.connect('TESTER ALL.db')
    c = conn.cursor()

    # Create tables
    c.execute('''CREATE TABLE Workers (
                    WorkerID INTEGER PRIMARY KEY,
                    Name TEXT NOT NULL,
                    RoleID INTEGER NOT NULL,
                    ContactNumber TEXT,
                    FOREIGN KEY (RoleID) REFERENCES Roles(RoleID)
                );''')

    c.execute('''CREATE TABLE Roles (
                    RoleID INTEGER PRIMARY KEY,
                    RoleName TEXT NOT NULL
                );''')

    c.execute('''CREATE TABLE Tasks (
                    TaskID INTEGER PRIMARY KEY,
                    WorkerID INTEGER NOT NULL,
                    TaskDesc TEXT,
                    TaskStatus TEXT,
                    ETA DATE,
                    TBatchID INTEGER,
                    FOREIGN KEY (TBatchID) REFERENCES Task_Batch(TBatchID),
                    FOREIGN KEY (WorkerID) REFERENCES Workers(WorkerID)
                );''')

    c.execute('''CREATE TABLE Notif (
                    NotifID INTEGER PRIMARY KEY,
                    WorkerID INTEGER NOT NULL,
                    TimeStamp TEXT,
                    NotifDesc TEXT,
                    FOREIGN KEY (WorkerID) REFERENCES Workers(WorkerID)
                );''')

    c.execute('''CREATE TABLE Accounts (
                    AccountID INTEGER PRIMARY KEY,
                    WorkerID INTEGER,
                    Email TEXT NOT NULL,
                    HashedPW TEXT NOT NULL,
                    Salt TEXT NOT NULL,
                    FOREIGN KEY (WorkerID) REFERENCES Workers(WorkerID)
                );''')

    c.execute('''CREATE TABLE Products (
                    ProductID INTEGER PRIMARY KEY,
                    ProductName TEXT NOT NULL,
                    Description TEXT,
                    Price REAL,
                    PreferredSupplierID INTEGER NOT NULL,
                    FOREIGN KEY (PreferredSupplierID) REFERENCES Suppliers(SupplierID)
                );''')

    c.execute('''CREATE TABLE Inventory (
                    Iventory_ID INTEGER PRIMARY KEY,
                    ProductID INTEGER NOT NULL,
                    PBatchID INTEGER,
                    StockQuantity INTEGER,
                    LocationID INTEGER,
                    FOREIGN KEY (PBatchID) REFERENCES Product_Batch(PBatchID),
                    FOREIGN KEY (ProductID) REFERENCES Products(ProductID),
                    FOREIGN KEY (LocationID) REFERENCES Locations(LocationID)
                );''')

    c.execute('''CREATE TABLE Locations (
                    LocationID INTEGER PRIMARY KEY,
                    LocationName TEXT NOT NULL
                );''')

    c.execute('''CREATE TABLE Suppliers (
                    SupplierID INTEGER PRIMARY KEY,
                    Name TEXT NOT NULL,
                    ContactNumber TEXT,
                    Email TEXT
                );''')

    c.execute('''CREATE TABLE Sales (
                    SaleID INTEGER PRIMARY KEY,
                    Date DATE
                );''')

    c.execute('''CREATE TABLE Sales_Inventory (
                    SaleID INTEGER NOT NULL,
                    ProductID INTEGER NOT NULL,
                    PBatchID INTEGER,
                    QuantitySold INTEGER,
                    UnitPrice REAL,
                    FOREIGN KEY (PBatchID) REFERENCES Product_Batch(PBatchID),
                    FOREIGN KEY (SaleID) REFERENCES Sales(SaleID),
                    FOREIGN KEY (ProductID) REFERENCES Products(ProductID)
                );''')

    c.execute('''CREATE TABLE Shipments (
                    ShipmentID INTEGER PRIMARY KEY,
                    ProductID INTEGER NOT NULL,
                    SupplierID INTEGER NOT NULL,
                    Quantity INTEGER NOT NULL,
                    ShipmentDate DATE NOT NULL,
                    FOREIGN KEY (ProductID) REFERENCES Products(ProductID),
                    FOREIGN KEY (SupplierID) REFERENCES Suppliers(SupplierID)
                );''')

    c.execute('''CREATE TABLE Product_Batch (
                    PBatchID INTEGER PRIMARY KEY,
                    PBatchDesc TEXT
                );''')

    c.execute('''CREATE TABLE Task_Batch (
                    TBatchID INTEGER PRIMARY KEY,
                    TBatchDesc TEXT
                );''')


    c.execute("INSERT INTO Roles (RoleName) VALUES ('Admin');")
    c.execute("INSERT INTO Roles (RoleName) VALUES ('Supervisor');")
    c.execute("INSERT INTO Roles (RoleName) VALUES ('Worker');")

    c.execute("INSERT INTO Product_Batch (PBatchID, PBatchDesc) VALUES (1, 'Batch 1');")
    c.execute("INSERT INTO Product_Batch (PBatchID, PBatchDesc) VALUES (2, 'Batch 2');")

    c.execute("INSERT INTO Task_Batch (TBatchID, TBatchDesc) VALUES (1, 'Batch 1');")
    c.execute("INSERT INTO Task_Batch (TBatchID, TBatchDesc) VALUES (2, 'Batch 2');")

    conn.commit()
    conn.close()
