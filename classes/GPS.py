import calendar
import datetime
import Logger

class GPS:
    def __init__(self):
        self.unix_time = 0
        self.N = 0.0
        self.E = 0.0
        self.ar_ratio = 0

    def parse_with_string(self, data):
        if data!="error":
            data = data.split("\t")
            date = datetime.datetime.strptime(data[0], "%Y/%m/%d %H:%M:%S.%f")
            self.unix_time = calendar.timegm(date.timetuple())
            self.N = float(data[1])
            self.E = float(data[2])
            self.ar_ratio = int(data[-1])
        else:
            self.unix_time = 0
            self.N = 0.0
            self.E = 0.0
            self.ar_ratio = 0

    def data_for_send(self):
        return struct.pack('= l d d b', *(self.unix_time, self.N, self.E, self.ar_ratio))
        # return struct.pack('= d d b', *(self.vehicle.gps_left.N, self.vehicle.gps_left.E, self.vehicle.gps_left.fix_q))
