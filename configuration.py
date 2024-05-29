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
        pass

    def getGraphicsPath(self) -> str:
        with open(self.config_file_path, "r") as f:
            return json.load(f)["Graphics"]

    def getDatabaseFile(self) -> str:
        with open(self.config_file_path, "r") as f:
            return json.load(f)["Database"]

    def getPreviewFile(self) -> str:
        with open(self.config_file_path, "r") as f:
            return json.load(f)["Preview"]

    def _updatePaths(self) -> None:
        data = {
            "Graphics" : f"{self.repo_file_path}/Graphics",
            "Database" : f"{self.repo_file_path}/Database.py",
            "Preview": f"{self.repo_file_path}/Frames/ui_preview_text.json"
        }

        with open(self.config_file_path, "w") as f:
            json.dump(data, f, indent=4)

if __name__ == "__main__":
    obj1 = Configuration()
    #print(obj1.getGraphicsPath())