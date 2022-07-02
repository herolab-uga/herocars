import time
import getch
import socket
import threading
import Controllers.CarController as CarController


def main_socket():

    car = CarController.CarController()
    control_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = ("127.0.0.1",5000)
    control_socket.bind(server_address)
    recv,_ = control_socket.listen(1)
    conn, addr = control_socket.accept()
    with conn:
        while True:
            command = conn.recv(1024)
            if command == 1:
                data = conn.recv(1024)
                car.p = data

            elif command == 2:
                data = conn.recv(1024)
                car.i = data

            elif command == 3:
                data = conn.recv(1024)
                car.d = data
                
            elif command == 4:
                conn.send(car.car_speed)
                
            elif command == 5:
                data = conn.recv(1024)
                car.min_speed = data

            elif command == 6:
                data = conn.recv(1024)
                car.max_speed = data

            elif command == 7:
                # need to send a list
                conn.send(c)

            elif command == 8:
                data = conn.recv(1024)
                car.line_color = data

            elif command == 9:
                data = conn.recv(1024)
                car.control_type = data

            elif command == 10:
                car.last_time = time.time()
                car.drive_forward()

            elif command == 11:
                car.last_time = time.time()
                car.drive_backward()

            elif command == 12:
                car.last_time = time.time()
                car.turn_left()

            elif command == 13:
                car.last_time = time.time()
                car.turn_right()

            else:
                car.stop()
                car.center_steering()

def main_manual():
    car = CarController.CarController()

    while True:
        ctl = getch.getch()
        if ctl == 'w':
            car.drive_forward()
        elif ctl == 's':
            car.drive_backward()
        elif ctl == 'a':
            car.turn_left()
        elif ctl == 'd':
            car.turn_right()



if __name__ == '__main__':
    main_manual()


