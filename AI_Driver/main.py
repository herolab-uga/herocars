import sys
from _thread import *
import threading
import time
from Controllers.CarController import CarController
import Socket.Client

car = CarController()


def drive(thread):
    car.StartCar()


def comm(thread):
    Socket.Client.TCP(car)


if __name__ == "__main__":
    try:
        # creating thread
        t1 = threading.Thread(target=drive, args=(10,))
        t2 = threading.Thread(target=comm, args=(10,))

        # starting thread 1
        t1.start()
        # starting thread 2
        t2.start()
    except Exception as e:
        print(e)
        sys.exit()
