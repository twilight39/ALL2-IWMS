import json
import os


class Configuration:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not isinstance(cls._instance, cls):
            cls._instance = super(Configuration, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        self.repo_file_path = f"{os.path.dirname(os.path.abspath(__file__))}"
        self.config_file_path = f"{os.path.dirname(os.path.abspath(__file__))}/config.json"
        self._updatePaths()

    def getGraphicsPath(self) -> str:
        with open(self.config_file_path, "r") as f:
            return json.load(f)["program_files"]["Graphics"]

    def getDatabaseFile(self) -> str:
        with open(self.config_file_path, "r") as f:
            return json.load(f)["program_files"]["Database"]

    def getPreviewFile(self) -> str:
        with open(self.config_file_path, "r") as f:
            return json.load(f)["program_files"]["Preview"]

    def getPreferences(self, employee_id: str) -> tuple[str, str]:
        try:
            with open(self.config_file_path, "r") as f:
                data = json.load(f)
                # print(json.load(f)["user_preferences"]["user_id"][str(employee_id)])
                preferences = tuple([data["user_preferences"]["user_id"][str(employee_id)]["profile_picture"],
                                    data["user_preferences"]["user_id"][str(employee_id)]["theme_name"]])
                return preferences

        except KeyError:
            self.writePreferences(str(employee_id))
            return self.getPreferences(employee_id)

    def writePreferences(self, employee_id: str, profile_picture: str = "default", theme_name: str = "default"):
        with open(self.config_file_path, "r") as f:
            data = json.load(f)

        try:
            test = data["user_preferences"]["user_id"][str(employee_id)]
            if profile_picture != "default":
                data["user_preferences"]["user_id"][str(employee_id)]["profile_picture"] = profile_picture
            if theme_name != "default":
                data["user_preferences"]["user_id"][str(employee_id)]["theme_name"] = theme_name

        except KeyError:
            data["user_preferences"]["user_id"][str(employee_id)] = {"profile_picture": "user_1a",
                                                                     "theme_name": "litera"}

        with open(self.config_file_path, "w") as f:
            json.dump(data, f, indent=4)

    def deletePreferences(self, employee_id: str):
        with open(self.config_file_path, "r") as f:
            data = json.load(f)

        try:
            del data["user_preferences"]["user_id"][str(employee_id)]
            print(data['user_preferences']['user_id'])
            with open(self.config_file_path, "w") as f:
                json.dump(data, f, indent=4)

        except KeyError:
            print('key error')
            return

    def _updatePaths(self) -> None:
        try:
            with open(self.config_file_path, "r") as f:
                data = json.load(f)

            data["program_files"] = {
                "Graphics": f"{self.repo_file_path}/Graphics",
                "Database": f"{self.repo_file_path}/Database/Database.db",
                "Preview": f"{self.repo_file_path}/Frames/ui_preview_text.json"
            }

        except FileNotFoundError:
            data = {
                "program_files": {
                    "Graphics": f"{self.repo_file_path}/Graphics",
                    "Database": f"{self.repo_file_path}/Database/Database.db",
                    "Preview": f"{self.repo_file_path}/Frames/ui_preview_text.json"
                },
                "user_preferences": {
                    "user_id": {
                    }
                }
            }

        with open(self.config_file_path, "w") as f:
            json.dump(data, f, indent=4)


if __name__ == "__main__":
    obj1 = Configuration()
    print(obj1.getPreferences('1'))
    # obj1.deletePreferences('1')
    #obj1.writePreferences('-1', theme_name="flatly")

