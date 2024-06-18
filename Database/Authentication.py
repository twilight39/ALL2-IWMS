import base64
import hashlib
import sqlite3

import bcrypt

from Database import singleton, DatabaseConnection


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

    def createAccount(self, employeeEmail: str, employeeRoleID: int, employeeName: str, employeeContactNumber: str ,employeePassword: str) -> bool:
        cursor = self.db_connection.cursor
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

    def updateAccount(self, employeeEmail: str, employeeRoleID: int, employeeName: str, employeeContactNumber: str ,
                      employeePassword: str, employeeID: int) -> bool:
        cursor = self.db_connection.cursor
        hashed = bcrypt.hashpw(base64.b64encode(hashlib.sha256(employeePassword.encode()).digest()),
                               bcrypt.gensalt(rounds=14))

        # Insert Account
        try:
            cursor.execute("""UPDATE Workers SET RoleID = ?, Name = ?, ContactNumber = ? WHERE WorkerID = ?""",
                           (employeeRoleID, employeeName, employeeContactNumber, employeeID,))
            cursor.execute("""UPDATE Accounts SET Email = ?, HashedPW = ? WHERE WorkerID = ?""",
                           (employeeEmail, hashed, employeeID))
            self.db_connection.connection.commit()
            return True

        except sqlite3.Error as e:
            print(f"Error:{e}")
            return False
