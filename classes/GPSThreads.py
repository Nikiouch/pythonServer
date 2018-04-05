import socket
import threading
import time

class ServerObj:
    def __init__(self, ip, port, timeout, socketType, type):
        self.BUFFER_SIZE = 1024
        self.option = (ip, port)
        self.recieveFunction = recieveFromSocket
        self.timeout = timeout
        self.socketType = socketType
        self.so = socket.socket(socket.AF_INET, self.socketType)
        self.err = False
        if self.socketType == socket.SOCK_STREAM:
            self.type = "TCP"
        self.stop = False
        self.type = type

    def stopServer(self):
        self.stop = True

    def initTcp(self):
        try:
            print (str(self.timeout)+" "+str(self.option)+" "+str(self.socketType))
            self.so = socket.socket(socket.AF_INET, self.socketType)
            self.so.settimeout(self.timeout)
            self.so.connect(self.option)
            return True
        except Exception as e:
            print (self.type + ": " + (" ".join([str(i) for i in e.args])))
            self.so.close()
            time.sleep(1)
            return False

    def server(self, vehicle):
        while not self.stop:
            connected = False
            self.err = False
            while (not connected) and (not self.stop):
                connected = self.initTcp()

            if self.recieveFunction != None:
                reciever = threading.Thread(target=self.recieveFunction, args=(self, vehicle,))
                reciever.start()

            while (not self.err) and (not self.stop):
                time.sleep(0.01)
            if self.recieveFunction != None:
                reciever.join()
            self.so.close()
        print (self.type + " server closed")

def recieveFromSocket(serverObj, vehicle):
    missings = 0
    while (not serverObj.stop) and (not serverObj.err):
        try:
            data = serverObj.so.recv(10000)
            if not data:
                missings=missings+1
            else:
                missings = 0
                # s=struct.Struct('= '+str(len(data))+'s')
                # data = s.unpack(data)[0]
                data=data.decode("utf-8")
                for message in data.split("\r\n"):
                    if message:
                        if serverObj.type == "left":
                            vehicle.gps_left.parse_with_string(data)
                        else:
                            vehicle.gps_right.parse_with_string(data)


            time.sleep(0.1)
        except Exception as e:
            print (str(e.args)+" recieve"+str(serverObj.type))
            if e.args[0]=='timed out':
                missings=missings+1
            else:
                serverObj.err = True;
        if missings > 5:
            if serverObj.type == "left":
                vehicle.gps_left.parse_with_string("error")
            else:
                vehicle.gps_right.parse_with_string("error")
            serverObj.err = True;
    return
