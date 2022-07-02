import getch
import socket

def main_manual():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect(("192.168.1.33",5000))
        while True:
            ctl = getch.getch()
            if ctl == 'w':
                s.send(10)
            elif ctl == 's':
                s.send(11)
            elif ctl == 'a':
                s.send(12)
            elif ctl == 'd':
                s.send(13)
            else:
                s.send(14)