import socket
import logging
import sys
import struct
import math
import os
import threading
import time
from socket import timeout
from collections import namedtuple
from classes import Vehicle
from classes import GPSThreads
from classes.TCPClientThread import ConnectionThread
import json

device_data = namedtuple("DeviceData", "conn addres ID timeout")






# ########### MAIN ##############
# ########### MAIN ##############
# ########### MAIN ##############
# ########### MAIN ##############
# ########### MAIN ##############
# ########### MAIN ##############
# ########### MAIN ##############



logging.basicConfig(filename="sample.log", level=logging.INFO, filemode="w")

# filename = {"clients": "clients_logs."}
# filename

clients = {}

vehicle = Vehicle()

timeoutNav = 1/2.0

left_IP = "192.168.80.101"
left_PORT = 11250

right_IP = "192.168.80.102"
right_PORT = 11250

left_gps = GPSThreads.ServerObj(left_IP, left_PORT, timeoutNav, socket.SOCK_STREAM, "left")
left_gps_client = threading.Thread(target=left_gps.server, args=(vehicle, ))
left_gps_client.start()

right_gps = GPSThreads.ServerObj(right_IP, right_PORT, timeoutNav, socket.SOCK_STREAM, "right")
right_gps_client = threading.Thread(target=right_gps.server, args=(vehicle, ))
right_gps_client.start()

threads = {}
not_connected = True
while not_connected:
    try:
        time.sleep(2)
        tcp_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        tcp_server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # tcp_server.bind(("192.168.80.30", 14900))
        tcp_server.bind(("localhost", 14900))
        tcp_server.listen(6)
        not_connected = False

    except KeyboardInterrupt:
        print("Exitting")
        not_connected = True

    except Exception as exp:
        not_connected = True
        print("rebind")


if not not_connected:
    try:
        while(1):
            (conn, addr) = tcp_server.accept()
            print("accept")
            id = conn.recv(10)
            if len(id)==8:
                id=id.split(b"\r")
                id = id[0].split(b"ID_")[1]
                print(id)
            elif len(id) == 10:
                id = id.split(b"\\")
                id = id[0].split(b"ID_")[1]
                print(id)
            elif len(id) == 6:
                id = id.split(b"ID_")[1]
                print(id)
            valid = False
            try:
                id = id.decode("utf - 8")
                id_int = int(id)
                valid = True
            except:
                valid = False
            if valid:
                clients[id] = True
                print(clients)
                threads[id] = (ConnectionThread(conn, addr, id_int, vehicle, 0.5, clients))
                threads[id].start()
                if id_int == 2:
                    vehicle.control.emergency = False
            else:
                conn.close()


    except KeyboardInterrupt:
        print("Exitting")
        tcp_server.close()
    except Exception as exp:
        print("Error"+str(exp.args[0]))
        tcp_server.close()

left_gps.stopServer()
right_gps.stopServer()
left_gps_client.join()
right_gps_client.join()
for key in threads.keys():
    threads[key].loseConnection()
    threads[key].join()
    print("Client with id "+key+" disconnected")
print("stopped")
