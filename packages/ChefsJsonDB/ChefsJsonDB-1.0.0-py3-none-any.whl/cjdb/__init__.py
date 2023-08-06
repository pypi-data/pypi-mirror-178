import json
import os


def createDB(path: str):
    if path == "":
        path = "./output.json"
    if not path.endswith(".json"):
        if path.endswith("/"):
            path += "output.json"
        else:
            path += ".json"
    if not os.path.exists(path):
        with open(path, "w") as f:
            f.close()
    return open(path, "a")


class DB:
    def __checkPath(path: str):
        if path == "":
            path = "./output.json"
        if not path.endswith(".json"):
            if path.endswith("/"):
                path += "output.json"
            else:
                path += ".json"
        return path

    def __init__(self, path: str):
        self.path = DB.__checkPath(path)
        self.file = createDB(path)
        self.content = ""

    def clearDB(self):
        self.content = ""

    def rewriteDB(self, t):
        self.content = json.loads(f'{json.dumps(t, indent=4)}')

    def addToDB(self, t):
        self.content.append(t)

    def getDB(self):
        data = self.content
        if data == "":
            data = "[]"
        data = json.loads(json.dumps(data))
        return data

    def updateDB(self):
        with open(self.path, "w") as f:
            if self.content == "":
                return None
            f.write(f'{json.dumps(self.content, indent=4)}')
            f.close()
