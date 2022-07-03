
import socket


def main_socket():
    control_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = ("",5000)
    control_socket.bind(server_address)
    control_socket.listen()
    conn, addr = control_socket.accept()
    with conn:
        while True:
            print(conn.recv().decode())

if __name__ == '__main__':
    main_socket()


