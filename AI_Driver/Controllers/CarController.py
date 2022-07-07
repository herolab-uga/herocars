from cv2 import VideoCapture, waitKey
import time
import threading
import RPi.GPIO as GPIO
from AI_Driver.AutoPhat.AutoPhatMD import AutoPhatMD

class CarController:

    def __init__(self) -> None:
        
        # Initialize the car

        # Autohat Object
        self._motor_driver = AutoPhatMD()

        self._min_speed = 0
        self._max_speed = 150
        
        self._line_color = 1 # 1: white, 0: black

        self._last_velo_time = 0 # last time the car was commanded to drive in manual mode
        self._last_steer_time = 0 # last time the car was commanded steer in manual mode

        self._p = 43       # Proportion value
        self._i = 1        # Integral Step value
        self._d = 13       # Derivative Step Value
        self._error = 0      # amount of _error on the line the car is experiencing
        self._prev_error = 0  # _error of last calculation used for Derivative calc
        self._straight = 1     # 1: _straight, 0: not _straight

        self._control_type = 0 # 0:Manual, 1:Auton

        self._PV = 0  # sum of all values errors that the car has experienced

        self._car_speed = 0 # speed of the car

        self._camera_frame = {
            "frame": None
        }

        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(29, GPIO.IN)  # RR IR Sensor
        GPIO.setup(31, GPIO.IN)  # RM IR Sensor
        GPIO.setup(33, GPIO.IN)  # MM IR Sensor
        GPIO.setup(35, GPIO.IN)  # LM IR Sensor
        GPIO.setup(37, GPIO.IN)  # LL IR Sensor

        # self.thread = threading.Thread(target=self.read_camera, args=(), daemon=True)
        # self.thread.start()

        # Create update thread
        update_thread = threading.Thread(target=self.auton_control_update,args=(),daemon=True)
        update_thread.start()

        # Create stop thread
        stop_thread = threading.Thread(target=self.car_auto_stop,args=(),daemon=True)
        stop_thread.start()

    # Create getter and setter methods for the last_time variable
    @property
    def last_velo_time(self):
        return self.last_time
    
    @last_velo_time.setter
    def last_velo_time(self, value):
        self._last_time = value

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

    # Gets the speed proportional to the _error
    def calculate_speed(self):
        self._car_speed = min(abs(int(abs(self._error) * self.maxSpeed /4)) + self.minSpeed, self.maxSpeed)
        return self._car_speed

    # Reads the frame from the camera
    def read_camera(self):
        # Create the video capture object
        cap = VideoCapture(0)

        # Loop until the camera is open
        while not cap.isOpened():
            pass

        # Loop until the camera is open
        while True:
            # Read the frame
            ret, self._camera_frame["frame"] = cap.read()

            # Wait for the user to press a key
            key = waitKey(30)

    # Gets the state of the car's line
    def get_line_state(self):
        # Get the states of the IR sensors
        line_state = [GPIO.input(37), GPIO.input(35), GPIO.input(33), GPIO.input(31), GPIO.input(29)]

        # If the line is set to white return the list
        if self._line_color == "white":
            return line_state
        # If the line is set to black return the list with the opposite values
        else:
            return [not x for x in line_state]

    def calculate_error(self):

        self.prevError = self._error

        # Combine IR sensors into _error value

        # Get the states of the IR sensors
        LL,LM,MM,RM,RR = self.get_line_state()

        self._error = (4*RR + 2*RM + 0 + -2*LM + -4*LL) / (RR + RM + MM + LM + LL)
        
        if abs(self._error) < 4:
            self._PV += -.0001 * self._error

        self._PV = max(self._PV,-10)
        self._PV = min(self._PV,10)
            
        return self._error

    def auton_control_update(self):
        while True:
            if self._control_type == 1:
                _error = self.calculate_error()
                correction = self._p * _error + self._i * self._PV + self._d * (self._error -self._prev_error)
                self.motorDriver.Turn(correction)
                self.motorDriver.Drive(self.calculate_speed())

    def car_auto_stop(self):
        while True:
            print(time.time() - self._last_velo_time)
            if self._control_type == 0 and time.time() - self._last_velo_time > .05 and not self._car_speed == 0:
                self.stop()
            if self._control_type == 0 and time.time() - self._last_steer_time > .05 and not self._straight:
                self.stragith = 1
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

