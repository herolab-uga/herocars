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

        self.control_variables ={
            "line_color":0,         # 1: white, 0: black
            "straight":1,
            "control_type":0        # 0:Manual, 1:Auton
        }

        self.speed = {
            "min":0,
            "max":150,
            "current_speed":0
        }

        self.last_times = {
            "last_velo_time":0,
            "last_steer_time":0
        }

        # Sets the PID values for the car
        self.pid_values = {
            "p":50,
            "i":50,
            "d":50,
            "errors":0,             # amount of _error on the line the car is experiencing
            "prev_error":0,         # _error of last calculation used for Derivative calc
            "PV":0
        }

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

    # Gets the speed proportional to the _error
    def calculate_speed(self):
        self._car_speed = min(abs(int(abs(self._error) * (self._max_speed /4))) + self._min_speed, self._max_speed)
        return self._car_speed

    # Reads the frame from the camera
    def read_camera(self):
        # Create the video capture object
        cap = cv2.VideoCapture(-1)

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
            if self._control_type == 1:
                _error = self.calculate_error()
                correction = self._p * _error + self._i * self._PV + self._d * (self._error -self._prev_error)
                self._motor_driver.Turn(correction)
                self._motor_driver.Drive(self.calculate_speed())

    def car_auto_stop(self):
        while True:
            if self._control_type == 0: 
                if time.time() - self._last_velo_time > .05 and not self._car_speed == 0 :
                    self.stop()
                if time.time() - self._last_steer_time > .05 and not self._straight:
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
        self._motor_driver.Stop()
    
    def center_steering(self):
        self._motor_driver.ManualSteerStop()

