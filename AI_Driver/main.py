import getch
import threading
import Controllers.CarController as CarController


def main():

    car = CarController.CarController()

    while True:
        ctl = getch.getch()
        if ctl == 'w':
            car.forward()
        elif ctl == 's':
            car.backward()
        elif ctl == 'a':
            car.left()
        elif ctl == 'd':
            car.right()

if __name__ == '__main__':
    main()


