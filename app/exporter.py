import json

class Exporter:
    def get_tempalte_json(self):
        with open("./templates/template.json", "rb") as f:
            templates = json.loads(f.read())
        return templates
