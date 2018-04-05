from classes.Radar import Radar
from classes.GPS import GPS
from classes.IMU import IMU
from classes.Sonar import Sonar
from classes.Control import Control

class Vehicle:
    def __init__(self):
        self.control = Control()
        self.imu = IMU()
        self.gps_left = GPS()
        self.gps_right = GPS()
        self.radar1 = Radar()
        self.radar2 = Radar()
        self.sonar = Sonar()
        self.vel = 0.0
        self.gear = 0
        self.acc = 0.0
        self.breaks = 0.0
        self.rpm = 0.0
        self.steer = 0.0

    def fill_with_stm(self, params):
        self.vel = params[2]
        self.gear = params[3]
        self.acc = params[4]
        self.breaks = params[5]
        self.rpm = params[6]
        # print(params)
