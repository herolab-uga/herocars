import getch
import socket

def main_manual():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect(("",5000))
        while True:
            ctl = getch.getch()
            if ctl == 'w':
                s.send("10".encode())
            elif ctl == 's':
                s.send("11".encode())
            elif ctl == 'a':
                s.send("12".encode())
            elif ctl == 'd':
                s.send("13".encode())
            else:
                s.send("14".encode())
            
if __name__ == "__main__":
    main_manual()