import time
import getch
import socket
import threading
import Controllers.CarController as CarController


def main_socket():

    car = CarController.CarController()
    control_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = ("192.168.1.33",5000)#("127.0.0.1",5000)
    control_socket.bind(server_address)
    control_socket.listen()
    conn, addr = control_socket.accept()
    with conn:
        while True:
            command = int(conn.recv(1024).decode())
            if command == 1:
                data = int(conn.recv(1024).decode())
                car.p = data

            elif command == 2:
                data = int(conn.recv(1024).decode())
                car.i = data

            elif command == 3:
                data = int(conn.recv(1024).decode())
                car.d = data
                
            elif command == 4:
                conn.send(car.car_speed)
                
            elif command == 5:
                data = int(conn.recv(1024).decode())
                car.min_speed = data

            elif command == 6:
                data = int(conn.recv(1024).decode())
                car.max_speed = data

            elif command == 7:
                # need to send a list
                conn.send(c)

            elif command == 8:
                data = int(conn.recv(1024).decode())
                car.line_color = data

            elif command == 9:
                data = int(conn.recv(1024).decode())
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

if __name__ == '__main__':
    main_socket()


