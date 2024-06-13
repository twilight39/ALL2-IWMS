import os
from Database import DatabaseConnection, authentication
from datetime import date

def populateTestTable(db_connection:DatabaseConnection):
    auth = authentication()
    for name, roleID, contactNumber, email, password in [
        ["John Doe", 2, "123-456-7890", "john@example.com", "JohnIsDumb"],
        ["Bob Johnson", 3, "444-789-0123" ,"bob.johnson@company.com", "BobTheBuilder"],
        ["Charlie Williams", 2, "333-567-8901" ,"charlie.williams@company.com", "KingCharlesTheSecond"]
    ]:
        auth.createAccount(
            adminID= 1,
            adminPassword="admin1234",
            employeeEmail=email,
            employeeName=name,
            employeeRoleID=roleID,
            employeeContactNumber=contactNumber,
            employeePassword= password
        )

    for name, contactNumber, email in [
        ["Techtronics Inc.", "sales@techtronics.com", "1234567890"],
        ["FitGear", "info@fitgear.com", "9876543210"],
        ["Gear & Bags", "orders@gearandbags.com", "5551234567"]
    ]:
        db_connection.add_vendor(name, contactNumber, email)
    print(db_connection.query_vendor())

    for description, eta, workerID, batchID in [
        ["Write documentation for new feature", "2024-05-30", 1, None],
        ["Fix login bug", "2024-05-28", 2, None],
        ["Review code for pull request", "2024-05-27", 3, None]
    ]:
        db_connection.add_task(description, eta, workerID, batchID)
    print(db_connection.query_task_table())

    db_connection.add_taskBatch("Batch 1", "TASK-240611-A",[1,2])
    db_connection.add_taskBatch("Batch 2", "TASK-240611-B",[3])
    db_connection.delete_taskBatch(2)
    db_connection.update_taskBatch(1, "Super Space Soup Rare", [1,3], 2)
    print(db_connection.query_taskBatch())

    for no, name, description, price, supplierID in [
        ["FUR-CHR-M-BR-001","Executive Office Chair", "Ergonomic chair with adjustable features", 349.99, 3],
        ["FUR-TBL-M-BR-001","Wooden Dining Table", "Sturdy table for 6 people", 299.99, 1],
        ["FUR-CHR-M-BL-001","Mesh Office Chair", "Breathable chair ideal for long work hours", 199.99, 3],
        ["FUR-CHR-M-BL-002","Bar Stool (Set of 2)", "Adjustable stools with padded seats", 149.99, 2],
        ["FUR-SOF-L-GR-001","Sofa Bed", "Convertible sofa that folds out to a bed", 499.99, 3]
    ]:
        db_connection.add_product(no, name, description, price, supplierID)

    db_connection.add_purchaseOrder(1, 30, 1, "BATCH-240526-A")
    db_connection.add_purchaseOrder(3, 15, 2, "BATCH-240524-A")
    db_connection.add_purchaseOrder(2, 2, 3, "BATCH-240524-A")
    db_connection.add_purchaseOrder(5, 34, 2, "BATCH-240527-A")
    db_connection.delete_purchaseOrder("SHIP-240602-C")
    print(db_connection.query_purchaseOrder())

    for number in [f"SHIP-{date.today().strftime('%y%m%d')}-{alphabet}" for alphabet in ["A", "B"]]:
        #print(number)
        db_connection.receive_inventory(number)

    db_connection.update_inventory("FUR-CHR-M-BR-001", "BATCH-240526-A", 1, 3, 15)
    db_connection.update_inventory("FUR-CHR-M-BL-001", "BATCH-240524-A", 1, 3, 8)

    #for productID, quantity in [[1, 20], [3, 10], [5, 3]]:
    #    db_connection.create_salesOrder(productID, quantity)

    #for saleNo, productNo, quantity in [
    #    [f"SALE-{date.today().strftime('%y%m%d')}-A", "FUR-CHR-M-BR-001", 20],
    #    [f"SALE-{date.today().strftime('%y%m%d')}-B", "FUR-CHR-M-BL-001", 10],
    #    [f"SALE-{date.today().strftime('%y%m%d')}-C", "FUR-SOF-L-GR-001", 3]
    #]:
    #    db_connection.add_salesOrder(saleNo,productNo,quantity)
    #print(db_connection.query_salesOrder_table())

    db_connection.add_notification(1, "Admin only noti")
    db_connection.add_notification(2, "Supervisor noti")
    db_connection.add_notification(3, "Worker noti 1")
    db_connection.add_notification(3, "Worker noti 2")

    print(f"Worker Visible Notifications: {db_connection.query_notification(3)}")
    print(f"Admin Visible Notifications: {db_connection.query_notification(1)}")

def authTest():
    auth = authentication()

    # Creates Accounts
    for name, roleID, contactNumber, email, password in [
        ["John Doe", 2, "123-456-7890", "john@example.com", "JohnIsDumb"],
        ["Bob Johnson", 3, "444-789-0123" ,"bob.johnson@company.com", "BobTheBuilder"],
        ["Charlie Williams", 2, "333-567-8901" ,"charlie.williams@company.com", "KingCharlesTheSecond"]
    ]:
        auth.createAccount(
            adminID= 1,
            adminPassword="admin1234",
            employeeEmail=email,
            employeeName=name,
            employeeRoleID=roleID,
            employeeContactNumber=contactNumber,
            employeePassword= password
        )
    print("Accounts created successfully.")

    # Authenticates Accounts
    if auth.authenticate("ahmad@gmail.com", "admin1234"):
        print("Admin authenticate success.")

    if auth.authenticate("john@example.com", "JohnIsDumb"):
        print("Supervisor authenticate success.")

    # Resets a Password
    auth.resetPassword(4, "KingCharlesTheThird")
    if auth.authenticate("charlie.williams@company.com", "KingCharlesTheThird"):
        print("Password changed successfully.")

    # Deletes an Account
    auth.deleteAccount(1, "admin1234", 2)
    print("Account deleted succesfully.")

if __name__ == "__main__":
    try:
        os.remove("Database.db")
    except:
        pass
    con = DatabaseConnection()
    populateTestTable(con)
    #con.add_product("Test Product", "TEeeest", 20, "2 - Something")
    #print(con.query_vendor())

    #authTest()

    pass