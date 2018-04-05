import json
class Logger:
    def __init__(self, filename):
        self.folder = "logs"
        self.log_name = filename

    def save_json_data(self, data):
        with open(self.folder+"/"+self.log_name, 'w') as outfile:
            json.dump(data, outfile)
