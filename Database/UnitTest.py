import os
from Database import DatabaseConnection, authentication

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
        ["Techtronics Inc.", "123-456-7890", "sales@techtronics.com"],
        ["FitGear", "987-654-3210", "info@fitgear.com"],
        ["Gear & Bags", "555-123-4567", "orders@gearandbags.com"]
    ]:
        db_connection.add_vendor(name, contactNumber, email)
    print(db_connection.query_vendor())

    for description, eta, workerID, batchID in [
        ["Write documentation for new feature", "2024-05-30", 1, None],
        ["Fix login bug", "2024-05-28", 2, None],
        ["Review code for pull request", "2024-05-27", 3, None]
    ]:
        db_connection.add_task(description, eta, workerID, batchID)
    print(db_connection.query_tasks())

    db_connection.add_taskBatch("Batch 1", [1,2])
    db_connection.add_taskBatch("Batch 2", [3])
    db_connection.delete_taskBatch(2)
    db_connection.update_taskBatch(1, "Super Space Soup Rare", [1,3], 2)
    print(db_connection.query_taskBatch())

    for id in ["240524-A", "240526-A", "240526-B"]:
        db_connection.add_productBatch(id)

    for name, description, price, supplierID in [
        ["Executive Office Chair", "Ergonomic chair with adjustable features", 349.99, 3],
        ["Wooden Dining Table", "Sturdy table for 6 people", 299.99, 1],
        ["Mesh Office Chair", "Breathable chair ideal for long work hours", 199.99, 3],
        ["Bar Stool (Set of 2)", "Adjustable stools with padded seats", 149.99, 2],
        ["Sofa Bed", "Convertible sofa that folds out to a bed", 499.99, 3]
    ]:
        db_connection.add_product(name, description ,price, supplierID)

    for productID, batchID, quantity in [
        [1, 1, 20],
        [2, 2, 50],
        [3, 2, 40]
    ]:
        db_connection.receive_product(productID, batchID, quantity)

    db_connection.update_product(2, 2, 1, 3, 15)
    db_connection.update_product(3, 2, 1, 4, 23)

    db_connection.add_purchaseOrder(2, 30, 1, 2)
    db_connection.add_purchaseOrder(3, 15, 2, 1)
    db_connection.add_purchaseOrder(1, 2, 3, 1)
    db_connection.delete_purchaseOrder(3)
    print(db_connection.query_purchaseOrder())

    db_connection.add_salesOrder(1, 1, 34)
    db_connection.add_salesOrder(2, 3, 19)
    db_connection.add_salesOrder(3, 2, 13)
    db_connection.update_salesOrder(1, 4, 2, 20)
    print(db_connection.query_salesOrder())

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
    #print(con.query_vendor())

    #authTest()

    pass