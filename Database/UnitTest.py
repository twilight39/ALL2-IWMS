import sqlite3
from Database import DatabaseConnection, authentication

def populateTestTable(db_connection:DatabaseConnection):
    for name, contactNumber, email in [
        ["Techtronics Inc.", "123-456-7890", "sales@techtronics.com"],
        ["FitGear", "987-654-3210", "info@fitgear.com"],
        ["Gear & Bags", "555-123-4567", "orders@gearandbags.com"]
    ]:
        db_connection.add_vendor(name, contactNumber, email)

    for description, eta, workerID, batchID in [
        ["Write documentation for new feature", "2024-05-30", None, None]
    ]:
        db_connection.add_task(description, eta, workerID, batchID)

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
    #con = DatabaseConnection()
    #populateTestTable(con)
    #print(con.query_vendor())
    #auth = authentication()
    #test()
    authTest()

