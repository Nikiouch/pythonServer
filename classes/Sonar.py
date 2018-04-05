class Sonar:
    def __init__(self):
        self.data = []
        for i in range(0, 16):
            self.data.append(0)

    def fill_with_array(self, params):
        for i in range(0, 16):
            self.data[i] = params[i+2]
