import threading
from threading import Thread
import struct
import socket
import time

class ConnectionThread(Thread):
    def __init__(self, conn, addr, id, vehicle, timeout, clients):

        Thread.__init__(self)
        self.conn = conn
        if timeout:
            self.conn.settimeout(timeout)
        self.addr = addr
        self.id = id
        self.vehicle = vehicle
        self.clients = clients
        self.stopped = False
        self.conn.setsockopt(socket.SOL_SOCKET,socket.SO_SNDBUF, 8000)

    def run(self):
        self.connection()

    def loseConnection(self):
        if (id == 2):
            self.vehicle.control.emergency = True
            
        self.conn.close()
        self.clients[str(self.id)] = False
        self.stopped = True

    def connection(self):
        print(self.addr)
        print(self.id)
        missed_packets = 0
        break_on_number_of_packets = 5
        while not self.stopped:
            try:
                if self.id == 0:
                    data = self.conn.recv(1024)
                    if not data:
                        missed_packets=missed_packets+1
                        if missed_packets == break_on_number_of_packets:
                            break
                    else:
                        missed_packets = 0
                        # print(data.split(b"\r\n"))
                        for message in data.split(b"\r\n"):
                            if message:
                                # s = struct.Struct('> s b f b f f b b b')
                                s = struct.Struct('> s b f b f f b b b b b')
                                params = s.unpack(message)
                                break
                        self.vehicle.control.fill_with_array_from_gamepad(params)

                elif self.id == 1:
                    data = self.conn.recv(1024)
                    packed_data = self.vehicle.control.pack_data_for_stm()
                    self.conn.send(packed_data)
                    if not data:
                        missed_packets=missed_packets+1
                        if missed_packets == break_on_number_of_packets:
                            break
                    else:
                        missed_packets = 0
                        # print(data.split(b"\r\n"))
                        for message in data.split(b"\r\n"):
                            if message:
                                s = struct.Struct('= s b f b f f f')
                                params = s.unpack(message)
                                self.vehicle.fill_with_stm(params)

                elif self.id == 2:
                    packed_data = self.vehicle.control.pack_data_for_stm()
                    self.conn.send(packed_data)
                    packed_data = struct.pack('= s b f f 2s', *(b"#", 10, self.vehicle.vel, self.vehicle.imu.angle_vel[2], b"\r\n"))
                    self.conn.send(packed_data)

                    data = self.conn.recv(1024)
                    if not data:
                        missed_packets=missed_packets+1
                        if missed_packets == break_on_number_of_packets:
                            break
                    else:
                        missed_packets = 0
                        for message in data.split(b"\r\n"):
                            if message:
                                s = struct.Struct('= b')
                                packet_number = s.unpack(message[1:2])[0]
                                if packet_number == 5:
                                    s = struct.Struct('= s b f')
                                    params = s.unpack(message)
                                    self.vehicle.steer = params[2]

                                if packet_number == 8:
                                    s = struct.Struct("= s b 16B")
                                    params = s.unpack(message)
                                    self.vehicle.sonar.fill_with_array(params)


                                if packet_number == 6:
                                    self.vehicle.radar1.reset_objects()
                                    s = struct.Struct('= s b b')
                                    number = s.unpack(message[:3])
                                    s = struct.Struct('= b 6f b 2f')
                                    if number[2]:
                                        for i in range(0, number[2]):
                                            params = s.unpack(message[3+(34*i):3+(34*i)+34])
                                            self.vehicle.radar1.parse_with_array(params)

                                if packet_number == 7:
                                    self.vehicle.radar2.reset_objects()
                                    s = struct.Struct('= s b b')
                                    number = s.unpack(message[:3])
                                    s = struct.Struct('= b 6f b 2f')
                                    if number[2]:
                                        for i in range(0, number[2]):
                                            params = s.unpack(message[3+(34*i):3+(34*i)+34])
                                            self.vehicle.radar2.parse_with_array(params)

                elif self.id == 3:
                    self.conn.send(struct.pack('= s b f 2s', *(b"#", 18, self.vehicle.vel, b"\r\n")))
                    if (self.vehicle.control.calibrate):
                        self.conn.send(struct.pack('= s b 2s', *(b"#", 3, b"\r\n")))
                        self.vehicle.control.calibrate = 0

                    data = self.conn.recv(20000)
                    if not data:
                        missed_packets=missed_packets+1
                        if missed_packets == break_on_number_of_packets:
                            break
                    else:
                        missed_packets = 0
                        for message in data.split(b"\r\n"):
                            if message:
                                s = struct.Struct('= b')
                                packet_number = s.unpack(message[1:2])[0]
                                if packet_number == 9:
                                    if len(message)==130:
                                        s = struct.Struct('= s b 4d 3d 3d 3d 3d')
                                        params = s.unpack(message)
                                        self.vehicle.imu.fill_with_stm(params)



                elif self.id == 4:
                    try:
                        data = self.conn.recv(1024)
                        if data:
                            if b'#' in data:
                                for message in data.split(b"#"):
                                    if message:
                                        s = struct.Struct('= b')
                                        packet_number = s.unpack(message[0:1])[0]
                                        if packet_number == 12:
                                            pack = []
                                            # pack.append( struct.pack('= d d b', *(self.vehicle.gps_left.N, self.vehicle.gps_left.E, self.vehicle.gps_left.fix_q)) )
                                            #
                                            # pack.append( struct.pack('= d d b', *(self.vehicle.gps_right.N, self.vehicle.gps_right.E, self.vehicle.gps_right.fix_q)) )

                                            pack.append( self.vehicle.gps_left.data_for_send())

                                            pack.append( self.vehicle.gps_right.data_for_send())

                                            pack.append( struct.pack('= f f f f f f', *(self.vehicle.imu.coord[0], self.vehicle.imu.coord[1], self.vehicle.imu.quat[0], self.vehicle.imu.quat[1], self.vehicle.imu.quat[2], self.vehicle.imu.quat[3])) )

                                            pack.append( struct.pack('= f f', *(self.vehicle.vel, self.vehicle.steer)) )

                                            sonar = b""
                                            for i in range(0,len(self.vehicle.sonar.data)):
                                                sonar = sonar+(struct.pack('= B', *(self.vehicle.sonar.data[i], )))
                                            pack.append(sonar)

                                            radar1 = b""
                                            if len(self.vehicle.radar1.objects):
                                                for i in range(0, len(self.vehicle.radar1.objects)):
                                                        obj = self.vehicle.radar1.objects[i]
                                                        radar1 = radar1+struct.pack('= b 6f b 2f', *(obj.self.id, obj.dist_long , obj.dist_lat, obj.vrel_long, obj.vrel_lat, obj.arel_long, obj.arel_lat, obj.class_number, obj.length, obj.wself.idth))
                                            pack.append( struct.pack('= b ', *(len(self.vehicle.radar1.objects), )))
                                            pack.append( radar1)

                                            radar2 = b""
                                            if len(self.vehicle.radar2.objects):
                                                for i in range(0, len(self.vehicle.radar2.objects)):
                                                        obj = self.vehicle.radar2.objects[i]
                                                        radar2 = radar2+struct.pack('= b 6f b 2f', *(obj.self.id, obj.dist_long , obj.dist_lat, obj.vrel_long, obj.vrel_lat, obj.arel_long, obj.arel_lat, obj.class_number, obj.length, obj.wself.idth))
                                            pack.append( struct.pack('= b ', *(len(self.vehicle.radar2.objects), )))
                                            pack.append( radar2)
                                            pack.append( struct.pack('= b f f f', *(self.vehicle.gear, self.vehicle.acc, self.vehicle.rpm, self.vehicle.breaks)) )
                                            # quant = sum(map(len, pack[:-1]))
                                            pack.append( struct.pack('= s b h', *(b"#", 13, len(pack[0]+pack[1]+pack[2]+pack[3]+pack[4]+pack[5]+pack[6]+pack[7]+pack[8]+pack[9])+4)))
                                            self.conn.send(pack[10]+pack[0]+pack[1]+pack[2]+pack[3]+pack[4]+pack[5]+pack[6]+pack[7]+pack[8]+pack[9])
                                            # print(len(pack[10]+pack[0]+pack[1]+pack[2]+pack[3]+pack[4]+pack[5]+pack[6]+pack[7]+pack[8]+pack[9]))
                                            # print(len(pack[0]+pack[1]+pack[2]+pack[3]+pack[4]+pack[5]+pack[6]+pack[7]+pack[8]+pack[9])+4)

                                        elif packet_number == 14:
                                            if len(message)==11:
                                                s = struct.Struct('= f f b b')
                                                params = s.unpack(message[1:11])
                                                self.vehicle.control.fill_with_array_from_adas(params)
                                        elif packet_number == 17:
                                            self.vehicle.control.calibrate = 1
                        else:
                            break;
                    except timeout:
                        # print("waiting")
                        time.sleep(0.01)
                    except Exception as exp:
                        print("Error"+str(exp.args[0])+" "+str(self.id))
                        break;

            except Exception as exp:
                    print("Error"+str(exp.args[0])+" "+str(self.id))
                    missed_packets = missed_packets+1
                    if missed_packets == break_on_number_of_packets:
                        break
            time.sleep(0.01)
        if not self.stopped:
            self.loseConnection()
        print("Client with id "+str(self.id)+" disconnected")
