class IMU:
    def __init__(self):
        self.quat = [0.0, 0.0, 0.0, 0.0]
        self.angle_vel = [0.0, 0.0, 0.5]
        self.acc = [0.0, 0.0, 0.0]
        self.vel = [0.0, 0.0, 0.0]
        self.coord = [0.0, 0.0, 0.0]

    def fill_with_stm(self, params):
        self.quat = params[2:6]
        self.angle_vel = params[6:9]
        self.acc = params[9:12]
        self.vel = params[12:15]
        self.coord = params[15:18]
