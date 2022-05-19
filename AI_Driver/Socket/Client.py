import sys
import socket
import os
import re
import time
import traceback

def get_ip_address():
 ip_address = '';
 s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
 s.connect(("8.8.8.8",80))
 ip_address = s.getsockname()[0]
 s.close()
 return ip_address

def TCP (car):
    hostname = socket.gethostname()
    host_addr = get_ip_address()
    carNum = 0
    oclet = host_addr.split('.')
    carNum = oclet[3]
    if (int(carNum) > 9):
        prefPort = '60'
    else:
        prefPort = '600'
    port = int(prefPort + carNum)
    if (port > 65535 or port < 1024):
      port = 1024 + carNum
    print(port)
    while True:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        ip = GetServerIP(carNum)
        print(ip)
        server_address = (ip, port)
        print(server_address)
        try:
            sock.connect(server_address)
        except Exception as e:
            print(e)
            os._exit(0)
        print("here")
        sock.settimeout(5)
        isConnected = True
        car.isConnected = True
        print("Connected")
        while isConnected:

            try:
                data = sock.recv(11, socket.MSG_WAITALL)
                print(data)
            except socket.timeout as e:
                car.isConnected = False
                isConnected = False
                print("closed")
                sock.close()
                break
            if not data: 
                break

            car.modifyPID(data)

            try:
                speed = car.speed
                if (speed < 0):
                    speed = 0
                elif (speed > 255):
                    speed = 255
                rList = [car.error + 10, speed]
                arr = bytearray(rList)
                sock.sendall(arr)

            except BrokenPipeError as e:
                car.isConnected = False
                isConnected = False
                print("closed")
                sock.close()
                os._exit(0)
        print("Looking")

def GetServerIP(deviceNumber):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    if (int(deviceNumber) > 9):
        prefPort = '06'
    else:
        prefPort = '006'
    port = int(deviceNumber + prefPort)
    if (port > 65535 or port < 1024):
      port = 1024 + int(deviceNumber)
    print(port)
    server_address = ('', port)
    sock.bind(server_address)
    data, address = sock.recvfrom(4096)
    sock.close()
    return address[0]
