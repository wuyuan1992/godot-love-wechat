import os
import json

class Storge:
    def __init__(self) -> None:
        self.path = os.path.join(os.environ['LOCALAPPDATA'], 'godot-love-wechat')

    def save(self, file, data):
        print(self.path)
        if not os.path.exists(self.path):
            os.mkdir(self.path)
        _data = json.dumps(data, indent=2)
        path = os.path.join(self.path, file)
        with open(path, "w+") as f:
            f.write(_data)

    def get(self, file):
        path = os.path.join(self.path, file)
        if not os.path.exists(path):
            return
        with open(path, "rb") as f:
            data = json.loads(f.read())
        return data

