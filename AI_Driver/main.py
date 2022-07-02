import getch
import threading
import Controllers.CarController as CarController


def main():

    car = CarController.CarController()

    while True:
        ctl = getch.getch()
        if ctl == 'w':
            car.drive_forward()
        elif ctl == 's':
            car.stop()
        elif ctl == 'a':
            car.turn_left()
        elif ctl == 'd':
            car.turn_right()

if __name__ == '__main__':
    main()


