from ttkbootstrap.toast import ToastNotification

from Database import DatabaseConnection
from configuration import Configuration
import json


class Notification:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not isinstance(cls._instance, cls):
            cls._instance = super(Notification, cls).__new__(cls)
        return cls._instance

    def __init__(self, employee_id: int):
        self.db_connection = DatabaseConnection()
        self.config = Configuration()
        self.notification_file = f"{self.config.repo_file_path}/Database/Notifications.json"
        self.employee_id = str(employee_id)
        self.role = self.db_connection.query_employee(employee_id)[1]

    def get_notifications(self):
        """Returns: [NotificationID, TimeStamp, Description]
        Excludes notifications based on Employee ID."""
        notifications = self.__read_notifications__()
        for exclusion in self.config.getNotificationExclusions(str(self.employee_id)):
            notifications = [notification for notification in notifications if str(notification[0]) != exclusion]
        return notifications

    def create_notification(self, notification_key: str, placeholder: str = None):
        """Creates a new notification. Placeholder is inserted if necessary."""
        with open(self.notification_file, "r") as f:
            data = json.load(f)[notification_key]

        if placeholder is not None:
            data["Message"] = data["Message"].format(placeholder)

        self._write_notification(data["Access"], data["Message"])

        dictionary = {"Worker": 3, "Supervisor": 2, "Administrator": 1}
        if dictionary[self.role] <= dictionary[(data["Access"])]:
            ToastNotification(title=data["Title"], message=data["Message"], duration=500).show_toast()

    def exclude_notification(self, notification_id: str) -> None:
        self.config.writeNotificationExclusions(self.employee_id, notification_id)

    def __read_notifications__(self):
        """Returns: [NotificationID, TimeStamp, Description]
        Does not consider excluded notifications."""
        return self.db_connection.query_notification(self.role)

    def _write_notification(self, role: str, message: str) -> int:
        """role: Access Level, message: Message -> notificationID: int"""
        return self.db_connection.add_notification(role, message)

    def __delete_notification__(self, notification_id: int):
        """Reference to delete a notification from the database."""
        self.db_connection.delete_notification(notification_id)


if __name__ == '__main__':
    # print(Notification(1).get_notifications())
    obj = Notification(1)
    obj.create_notification("New Product Added", f"Executive Office Chair")
