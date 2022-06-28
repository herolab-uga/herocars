import RPi.GPIO as GPIO
from AutoPhat.AutoPhatMD import AutoPhatMD

class CarController:

    def __init__(self) -> None:
        
        # Initialize the car
        # Autohat Object
        self.motor_driver = AutoPhatMD()

        self.steeringM = 0
        self.drivingM = 0

        self.direction = 0

        self.prev_steer = 0
        self.prev_drive = 0

        self.socket = 0

        self.max_speed = 150
        self.min_speed

        self.car_stopped = True
        self.line_color = 0

        self.__p = 43       # Proportion value
        self.__i = 1        # Integral Step value
        self.__d = 13       # Derivative Step Value
        self.error = 0      # amount of error on the line the car is experiencing

        self.control_type = 0
        self.car_speed = 0
        self.timer = False
        self.isPID = 0

        self.PV = 0  # sum of all values errors that the car has experienced

        self.prevError = 0  # error of last calculation used for Derivative calc

        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(29, GPIO.IN)  # RR IR Sensor
        GPIO.setup(31, GPIO.IN)  # RM IR Sensor
        GPIO.setup(33, GPIO.IN)  # MM IR Sensor
        GPIO.setup(35, GPIO.IN)  # LM IR Sensor
        GPIO.setup(37, GPIO.IN)  # LL IR Sensor

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

    # Create getter and setter methods for the car's control_type
    @property
    def control_type(self):
        return self.__control_type
    
    @control_type.setter
    def control_type(self, value):
        self.__control_type = value

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
    def speed(self):
        return min(abs(int(abs(self.error) * self.maxSpeed /4)) + self.minSpeed, self.maxSpeed)

    def calculate_error(self):

        self.prevError = self.error

        # Combine IR sensors into error value
        if self.line_color == 1:

            # Get the states of the IR sensors
            # If the line color is white, the IR sensors will turn on when the line is detected
            RR = GPIO.input(29)  # Right Right Sensor
            RM = GPIO.input(31)  # Right Middle Sensor
            MM = GPIO.input(33)  # Middle Middle Sensor
            LM = GPIO.input(35)  # Left Middle Sensor
            LL = GPIO.input(37)  # Left Left Sensor

            self.error = (4*RR + 2*RM + 0 + -2*LM + -4*LL) / (RR + RM + MM + LM + LL)
        else:

            # If the line color is white, the IR sensors will turn on when the line is not detected
            RR = not GPIO.input(29)  # Right Right Sensor
            RM = not GPIO.input(31)  # Right Middle Sensor
            MM = not GPIO.input(33)  # Middle Middle Sensor
            LM = not GPIO.input(35)  # Left Middle Sensor
            LL = not GPIO.input(37)  # Left Left Sensor

            self.error = (4*RR + 2*RM + 0 + -2*LM + -4*LL) / (RR + RM + MM + LM + LL)
        
        if abs(self.error) < 4:
            self.PV += -.0001 * self.error

    def turn_left(self):
        self.motor_driver.ManualLeft()
    
    def turn_right(self):
        self.motor_driver.ManualRight()
    
    def drive_forward(self):
        self.motor_driver.ManualForward()
    
    def drive_backward(self):
        self.motor_driver.ManualReverse()

