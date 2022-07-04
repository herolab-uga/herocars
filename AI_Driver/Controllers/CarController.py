import time
import threading
import RPi.GPIO as GPIO
from AutoPhat.AutoPhatMD import AutoPhatMD

class CarController:

    def __init__(self) -> None:
        
        # Initialize the car

        # Autohat Object
        self.motor_driver = AutoPhatMD()

        self.min_speed = 0
        self.max_speed = 150
        
        self.line_color = 1 # 1: white, 0: black

        self.last_velo_time = 0 # last time the car was commanded to drive in manual mode
        self.last_steer_time = 0 # last time the car was commanded steer in manual mode

        self.p = 43       # Proportion value
        self.i = 1        # Integral Step value
        self.d = 13       # Derivative Step Value
        self.error = 0      # amount of error on the line the car is experiencing
        self.prev_error = 0  # error of last calculation used for Derivative calc
        self.straight = 1     # 1: straight, 0: not straight

        self.control_type = 0 # 0:Manual, 1:Auton

        self.PV = 0  # sum of all values errors that the car has experienced

        self.car_speed = 0 # speed of the car

        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(29, GPIO.IN)  # RR IR Sensor
        GPIO.setup(31, GPIO.IN)  # RM IR Sensor
        GPIO.setup(33, GPIO.IN)  # MM IR Sensor
        GPIO.setup(35, GPIO.IN)  # LM IR Sensor
        GPIO.setup(37, GPIO.IN)  # LL IR Sensor

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
    def last_vel_time(self, value):
        self.last_time = value

    # Create getter and setter methods for the last_steer_time variable
    @property
    def last_steer_time(self):
        return self.last_steer_time

    @last_steer_time.setter
    def last_steer_time(self, value):
        self.last_steer_time = value

    # Create getter and setter methods for the car's p, i, and d
    @property
    def p(self):
        return self.p

    @p.setter
    def p(self, value):
        self.p = value
    
    @property
    def i(self):
        return self.i
    
    @i.setter
    def i(self, value):
        self.i = value
    
    @property
    def d(self):
        return self.d
    
    @d.setter
    def d(self, value):
        self.d = value  

    # Create getter and setter methods for the car's car_speed
    @property
    def car_speed(self):
        return self.car_speed
    
    @car_speed.setter
    def car_speed(self, value):
        self.car_speed = value
    
    # Create getter and setter methods for the car's line_color
    @property
    def line_color(self):
        return self.line_color
    
    @line_color.setter
    def line_color(self, value):
        self.line_color = value

    # Create getter and setter methods for the car's error
    @property
    def error(self):
        return self.error
    
    @error.setter
    def error(self, value):
        self.error = value

    # Create getter and setter methods for the car's min_speed
    @property
    def min_speed(self):
        return self.min_speed
    
    @min_speed.setter
    def min_speed(self, value):
        self.min_speed = value
    
    # Create getter and setter methods for the car's max_speed
    @property
    def max_speed(self):
        return self.max_speed
    
    @max_speed.setter
    def max_speed(self, value):
        self.max_speed = value

    # Create getter and setter methods for the car's control_type
    @property
    def control_type(self):
        return self.control_type
    
    @control_type.setter
    def control_type(self, value):
        self.control_type = value   

    # Gets the speed proportional to the error
    def calculate_speed(self):
        self.car_speed = min(abs(int(abs(self.error) * self.maxSpeed /4)) + self.minSpeed, self.maxSpeed)
        return self.car_speed

    # Gets the state of the car's line
    def get_line_state(self):
        # Get the states of the IR sensors
        line_state = [GPIO.input(37), GPIO.input(35), GPIO.input(33), GPIO.input(31), GPIO.input(29)]

        # If the line is set to white return the list
        if self.line_color == "white":
            return line_state
        # If the line is set to black return the list with the opposite values
        else:
            return [not x for x in line_state]

    def calculate_error(self):

        self.prevError = self.error

        # Combine IR sensors into error value

        # Get the states of the IR sensors
        LL,LM,MM,RM,RR = self.get_line_state()

        self.error = (4*RR + 2*RM + 0 + -2*LM + -4*LL) / (RR + RM + MM + LM + LL)
        
        if abs(self.error) < 4:
            self.PV += -.0001 * self.error

        self.PV = max(self.PV,-10)
        self.PV = min(self.PV,10)
            
        return self.error

    def auton_control_update(self):
        while True:
            if self.control_type == 1:
                error = self.calculate_error()
                correction = self.p * error + self.i * self.PV + self.d * (self.error -self.prev_error)
                self.motorDriver.Turn(correction)
                self.motorDriver.Drive(self.calculate_speed())

    def car_auto_stop(self):
        while True:
            if self.control_type == 0 and time.time() - self.last_velo_time > .05 and not self.car_speed == 0:
                self.stop()
            if self.control_type == 0 and time.time() - self.last_steer_time > .05 and not self.straight:
                self.stragith = 1
                self.center_steering()
            time.sleep(.01)

    def turn_left(self):
        self.motor_driver.ManualLeft()
    
    def turn_right(self):
        self.motor_driver.ManualRight()
    
    def drive_forward(self):
        self.motor_driver.ManualForward()
    
    def drive_backward(self):
        self.motor_driver.ManualReverse()
    
    def stop(self):
        self.car_speed = 0
        self.motor_driver.ManualDriveStop()
    
    def center_steering(self):
        self.motor_driver.ManualSteerStop()

