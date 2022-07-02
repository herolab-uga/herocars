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

        self.last_time = 0 # last time the car was commanded in manual mode

        self.__p = 43       # Proportion value
        self.__i = 1        # Integral Step value
        self.__d = 13       # Derivative Step Value
        self.error = 0      # amount of error on the line the car is experiencing
        self.prevError = 0  # error of last calculation used for Derivative calc

        self.control_type = 0 # 0:Manual, 1:Auton

        self.PV = 0  # sum of all values errors that the car has experienced

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
    def last_time(self):
        return self.__last_time
    
    @last_time.setter
    def last_time(self, value):
        self.__last_time = value

    # Create getter and setter methods for the car's __p, __i, and __d
    @property
    def p(self):
        return self.__p
    
    @p.setter
    def p(self, value):
        self.__p = value
    
    @property
    def i(self):
        return self.__i
    
    @i.setter
    def i(self, value):
        self.__i = value
    
    @property
    def d(self):
        return self.__d
    
    @d.setter
    def d(self, value):
        self.__d = value  

    # Create getter and setter methods for the car's car_speed
    @property
    def car_speed(self):
        return self.__car_speed
    
    @car_speed.setter
    def car_speed(self, value):
        self.__car_speed = value
    
    # Create getter and setter methods for the car's line_color
    @property
    def line_color(self):
        return self.__line_color
    
    @line_color.setter
    def line_color(self, value):
        self.__line_color = value

    # Create getter and setter methods for the car's error
    @property
    def error(self):
        return self.__error
    
    @error.setter
    def error(self, value):
        self.__error = value

    # Create getter and setter methods for the car's min_speed
    @property
    def min_speed(self):
        return self.__min_speed
    
    @min_speed.setter
    def min_speed(self, value):
        self.__min_speed = value
    
    # Create getter and setter methods for the car's max_speed
    @property
    def max_speed(self):
        return self.__max_speed
    
    @max_speed.setter
    def max_speed(self, value):
        self.__max_speed = value

    # Create getter and setter methods for the car's control_type
    @property
    def control_type(self):
        return self.__control_type
    
    @control_type.setter
    def control_type(self, value):
        self.__control_type = value   

    # Gets the speed proportional to the error
    def calculate_speed(self):
        return min(abs(int(abs(self.error) * self.maxSpeed /4)) + self.minSpeed, self.maxSpeed)

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
                correction = self.__p * error + self.__i * self.PV + self.__d * (self.error -self.prev_error)
                self.motorDriver.Turn(correction)
                self.motorDriver.Drive(self.calulate_speed())

    def car_auto_stop(self):
        while True:
            print(self.last_time)
            if self.control_type == 0 and time.time() - self.last_time > 10:
                self.center_steering()
                self.stop()

    def turn_left(self):
        self.motor_driver.ManualLeft()
    
    def turn_right(self):
        self.motor_driver.ManualRight()
    
    def drive_forward(self):
        self.motor_driver.ManualForward()
    
    def drive_backward(self):
        self.motor_driver.ManualReverse()
    
    def stop(self):
        self.motor_driver.ManualDriveStop()
    
    def center_steering(self):
        self.motor_driver.ManualSteerStop()

