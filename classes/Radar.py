class Radar:
    def __init__(self):
        self.objects = []

    def parse_with_array(self, params):
        object = RadarObject()
        object.parse_with_array(params)
        self.objects.append(object)

    def reset_objects(self):
        self.objects = []


class RadarObject:
    def __init__(self):
        self.id = 0
        self.dist_long = 0.0
        self.dist_lat = 0.0
        self.vrel_long = 0.0
        self.vrel_lat = 0.0
        self.arel_long = 0.0
        self.arel_lat = 0.0
        self.class_number = 0
        self.length = 0.0
        self.width = 0.0

    def parse_with_array(self, params):
        self.id = params[0]
        self.dist_long = params[1]
        self.dist_lat = params[2]
        self.vrel_long = params[3]
        self.vrel_lat = params[4]
        self.arel_long = params[5]
        self.arel_lat = params[6]
        self.class_number = params[7]
        self.length = params[8]
        self.width = params[9]
