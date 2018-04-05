import struct
import Logger

class Control:
    def __init__(self):
        # self.logger = Logger("control.txt")
        self.steer = 0.0
        self.gear = 0
        self.acc = 0.0
        self.breaks = 0.0
        self.autopilot = 0
        self.drive_control = 0
        self.calibrate = 0
        self.turn_light = 0
        self.light = 0
        self.emergency = False

    def pack_data_for_stm(self):
        packed_data = struct.pack('= s b b f f b f b b 2s', *(b"#", 1, control.drive_control, control.acc, control.breaks, control.gear, control.steer, control.turn_light, control.light,  b"\r\n"))
        # data = self.__dict__
        # self.logger.save_json_data(data)
        return packed_data

    def fill_with_array_from_adas(self, params):
        if (self.autopilot) and (self.drive_control):
            self.steer = params[0]
            if params[1] > 0:
                self.acc = params[1]
                self.breaks = 0
            else:
                self.acc = 0
                self.breaks = params[1]
            self.gear = params[2]
            self.turn_light = params[3]

            if self.emergency:
                self.acc = 0
                self.breaks = -9

    def fill_with_array_from_gamepad(self, params):
        self.drive_control = params[7]
        self.autopilot = params[6]
        if (not self.autopilot) and ( self.drive_control):
            self.steer = params[2]
            self.gear = params[3]
            self.acc = params[4]
            self.breaks = params[5]
            self.calibrate = params[8]
            self.turn_light = params[9]
            self.light = params[10]
        if self.emergency:
            self.acc = 0
            self.breaks = -9
