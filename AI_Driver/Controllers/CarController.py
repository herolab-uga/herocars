from socketserver import ThreadingUnixDatagramServer
import cv2
import time
import threading
import queue
import RPi.GPIO as GPIO
from AI_Driver.AutoPhat.AutoPhatMD import AutoPhatMD

class CarController:

    def __init__(self) -> None:
        # Initialize the car

        # Autohat Object
        self._motor_driver = AutoPhatMD()

        self._min_speed = 0
        self._max_speed = 150
        self._line_color = "White" # 1: white, 0: black

        self._last_velo_time = 0 # last time the car was commanded to drive in manual mode
        self._last_steer_time = 0 # last time the car was commanded steer in manual mode

        self._p = 43       # Proportion value
        self._i = 1        # Integral Step value
        self._d = 13       # Derivative Step Value
        self._error = 0      # amount of _error on the line the car is experiencing
        self._prev_error = 0  # _error of last calculation used for Derivative calc
        self._straight = 1     # 1: _straight, 0: not _straight

        self._control_type = "Auton" # 0:Manual, 1:Auton

        self._PV = 0  # sum of all values errors that the car has experienced

        self._car_speed = 0 # speed of the car

        self._camera_queue = queue.Queue(maxsize=1)

        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(29, GPIO.IN)  # RR IR Sensor
        GPIO.setup(31, GPIO.IN)  # RM IR Sensor
        GPIO.setup(33, GPIO.IN)  # MM IR Sensor
        GPIO.setup(35, GPIO.IN)  # LM IR Sensor
        GPIO.setup(37, GPIO.IN)  # LL IR Sensor

        self.thread = threading.Thread(target=self.read_camera, args=(), daemon=True)
        self.thread.start()

        # Create update thread
        update_thread = threading.Thread(target=self.auton_control_update,args=(),daemon=True)
        update_thread.start()

        # # Create stop thread
        stop_thread = threading.Thread(target=self.car_auto_stop,args=(),daemon=True)
        stop_thread.start()

    # Create getter and setter methods for the last_time variable
    @property
    def last_velo_time(self):
        return self.last_velo_time

    @last_velo_time.setter
    def last_velo_time(self, value):
        self._last_velo_time = value

    # Create getter and setter methods for the _last_steer_time variable
    @property
    def last_steer_time(self):
        return self._last_steer_time

    @last_steer_time.setter
    def last_steer_time(self, value):
        self._last_steer_time = value

    # Create getter and setter methods for the car's _p, _i, and _d
    @property
    def p(self):
        return self._p

    @p.setter
    def p(self, value):
        self._p = value

    @property
    def i(self):
        return self._i

    @i.setter
    def i(self, value):
        self._i = value

    @property
    def d(self):
        return self._d

    @d.setter
    def d(self, value):
        self._d = value

    # Create getter and setter methods for the car's _car_speed
    @property
    def car_speed(self):
        return self._car_speed

    @car_speed.setter
    def car_speed(self, value):
        self._car_speed = value

    # Create getter and setter methods for the car's _line_color
    @property
    def line_color(self):
        return self._line_color

    @line_color.setter
    def line_color(self, value):
        self._line_color = value

    # Create getter and setter methods for the car's _error
    @property
    def error(self):
        return self._error

    @error.setter
    def error(self, value):
        self._error = value

    # Create getter and setter methods for the car's _min_speed
    @property
    def min_speed(self):
        return self._min_speed

    @min_speed.setter
    def min_speed(self, value):
        self._min_speed = value
    
    # Create getter and setter methods for the car's _max_speed
    @property
    def max_speed(self):
        return self._max_speed
    
    @max_speed.setter
    def max_speed(self, value):
        self._max_speed = value

    # Create getter and setter methods for the car's _control_type
    @property
    def control_type(self):
        return self._control_type
    
    @control_type.setter
    def control_type(self, value):
        self._control_type = value

    # Create getter for the camera frame
    @property
    def camera_frame(self):
        return self._camera_frame

    # Create getter for the _straight variable
    @property
    def straight(self):
        return self._straight 

    # Create setter for the _straight variable
    @straight.setter
    def straight(self, value):
        self._straight = value

    # Gets the speed proportional to the _error
    def calculate_speed(self):
        self._car_speed = min(abs(int(abs(self._error) * (self._max_speed /4))) + self._min_speed, self._max_speed)
        return self._car_speed

    # Reads the frame from the camera
    def read_camera(self):
        # Create the video capture object
        cap = cv2.VideoCapture(0)

        # Loop until the camera is open
        while not cap.isOpened():
            pass

        # Loop until the camera is open
        while True:
            # Read the frame
            success,frame = cap.read()

            if not success:
                continue

            if self._camera_queue.empty():
                self._camera_queue.put(frame)
                

    def get_frame(self):
        while True:
            frame = self._camera_queue.get()
            ret,buffer = cv2.imencode('.jpg',frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  # concat frame one by one and show result

    # Gets the state of the car's line
    def get_line_state(self):
        # Get the states of the IR sensors
        line_state = [GPIO.input(37), GPIO.input(35), GPIO.input(33), GPIO.input(31), GPIO.input(29)]

        # If the line is set to white return the list
        if self._line_color == "White":
            return line_state
        # If the line is set to black return the list with the opposite values
        else:
            return [not x for x in line_state]

    def calculate_error(self):

        self.prevError = self._error

        # Combine IR sensors into _error value

        # Get the states of the IR sensors
        LL,LM,MM,RM,RR = self.get_line_state()
        try:
            self._error = (4*RR + 2*RM + 0 + -2*LM + -4*LL) / (RR + RM + MM + LM + LL)
        except ZeroDivisionError:
            print("not on line")
        if abs(self._error) < 4:
            self._PV += -.0001 * self._error

        self._PV = max(self._PV,-10)
        self._PV = min(self._PV,10)
            
        return self._error

    def auton_control_update(self):
        while True:
            if self._control_type == "Autonomous":
                _error = self.calculate_error()
                correction = self._p * _error + self._i * self._PV + self._d * (self._error -self._prev_error)
                self._motor_driver.Turn(correction)
                self._motor_driver.Drive(self.calculate_speed())

    def car_auto_stop(self):
        while True:
            if self._control_type == 0 and time.time() - self._last_velo_time > .05 and not self._car_speed == 0 :
                self.stop()
            if self._control_type == 0 and time.time() - self._last_steer_time > .05 and not self._straight:
                self._straight = 1
                self.center_steering()
            time.sleep(.01)

    def turn_left(self):
        self._motor_driver.ManualLeft()
    
    def turn_right(self):
        self._motor_driver.ManualRight()
    
    def drive_forward(self):
        self._motor_driver.ManualForward()
    
    def drive_backward(self):
        self._motor_driver.ManualReverse()
    
    def stop(self):
        self._car_speed = 0
        self._motor_driver.ManualDriveStop()
    
    def center_steering(self):
        self._motor_driver.ManualSteerStop()

