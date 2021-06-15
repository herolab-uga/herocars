import RPi.GPIO as GPIO
from time import sleep
import sys
import socket
from datetime import datetime
from AutoPhat.AutoPhatMD import AutoPhatMD
import os
import qwiic_icm20948
import threading

class CarController:
    IMU = qwiic_icm20948.QwiicIcm20948()
    isConnected = False
    motorDriver = AutoPhatMD()
    steeringM = 0
    drivingM = 0
    direction = 0
    prevSteer = 0
    prevDrive = 0
    socket = 0
    maxSpeed = 150
    carStopped = True
    lineColor = 0
    J_P = 43 # Proportion value
    J_I = 1 # Integral Step value
    J_D = 13  # Derivative Step Value
    error = 0  # amount of error on the line the car is experiencing
    controlType = 0
    speed = 0
    timer = False
    isPID = 0
    PV = 0  # list of all values errors that the car has experienced
    prevError = 0  # error of last calculation used for Derivative calc
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(29, GPIO.IN)  # RR IR Sensor
    GPIO.setup(31, GPIO.IN)  # RM IR Sensor
    GPIO.setup(33, GPIO.IN)  # MM IR Sensor
    GPIO.setup(35, GPIO.IN)  # LM IR Sensor
    GPIO.setup(37, GPIO.IN)  # LL IR Sensor
    minSpeed = 75
    IMU.begin()
    def Speed(self):  # Gets speed proportional to error term
        speed = int(abs(self.error) *self.maxSpeed /4) + self.minSpeed
        if (speed > self.maxSpeed):
            return self.maxSpeed
        return speed
    def Proportion(self):  # Calculates P of PID multiplied by the its constant
        return (self.error * self.J_P)

    def Integral(self):  # Calculates I of PID multiplied by the its constant
        if (self.PV > 10):
            self.PV = 10
        if (self.PV < -10):
            self.PV = -10
        return (self.J_I * self.PV)
    def Derivative(self):  # Caluclates D of PID multiplied by the its constant
        return ((self.error - self.prevError) * self.J_D)

    def PID(self):  # Returns PID model
        return (self.Proportion() -  self.Integral() - self.Derivative())
    def modifyPID(self, newConstants):
        self.minSpeed = newConstants[0]
        self.turningDegree = newConstants[1]
        self.drivingDegree = newConstants[2]
        if (self.direction == 1):
            self.turningDegree = self.turningDegree * -1
        self.J_P = newConstants[3]
        self.J_I = newConstants[4]
        self.J_D = newConstants[5]
        self.controlType = newConstants[6]
        self.steeringM = newConstants[7]
        self.drivingM = newConstants[8]
        self.lineColor = newConstants[9]
        self.maxSpeed = newConstants[10]
    def DisconnectCar(self):
        self.motorDriver.Stop()
        os._exit(0)
    def getError(self):
        if (self.error != -5):
            self.prevError = self.error
        if (self.lineColor == 0):
            line = 0
            noLine = 1
        else:
            line = 1
            noLine = 0
        
        RR = GPIO.input(29)  # Right Right Sensor
        RM = GPIO.input(31)  # Right Middle Sensor
        MM = GPIO.input(33)  # Middle Middle Sensor
        LM = GPIO.input(35)  # Left Middle Sensor
        LL = GPIO.input(37)  # Left Left Sensor
        # 0 0 0 0 1 ==> Error = 4
        # 0 0 0 1 1 ==> Error = 3
        # 0 0 0 1 0 ==> Error = 2
        # 0 0 1 1 0 ==> Error = 1
        # 0 0 1 0 0 ==> Error = 0
        # 0 1 1 0 0 ==> Error = -1
        # 0 1 0 0 0 ==> Error = -2
        # 1 1 0 0 0 ==> Error = -3
        # 1 0 0 0 0 ==> Error = -4
        if (LL == noLine and LM == noLine and MM == noLine and RM == noLine and RR == line):
            self.error = 4
        elif (LL == noLine and LM == noLine and MM == noLine and RM == line and RR == line):
            self.error = 3
        elif (LL == noLine and LM == noLine and MM == noLine and RM == line and RR == noLine):
            self.error = 2
        elif (LL == noLine and LM == noLine and MM == line and RM == line and RR == noLine):
            self.error = 1
        elif (LL == noLine and LM == noLine and MM == line and RM == noLine and RR == noLine):
            self.error = 0
        elif (LL == noLine and LM == line and MM == line and RM == noLine and RR == noLine):
            self.error = -1
        elif (LL == noLine and LM == line and MM == noLine and RM == noLine and RR == noLine):
            self.error = -2
        elif (LL == line and LM == line and MM == noLine and RM == noLine and RR == noLine):
            self.error = -3
        elif (LL == line and LM == noLine and MM == noLine and RM == noLine and RR == noLine):
            self.error = -4
        else:
            self.error = -5
        if (self.error != -5):
            self.PV +=  -.0001 * self.error
        #print(str(LL) + " " + str(LM) + " " + str(MM) + " " + str(RM) + " " + str(RR))
        #print(self.error)
        return self.error
    def driveCar(self, motor):
        while (True):
            if (self.isConnected):
                if (motor == 0):
                    self.error = self.getError()
                if (self.controlType == 0):
                    if (self.error == -5):
                        if (self.speed != 0):
                            self.speed = self.speed - 50
                        else:
                            self.speed = 0
                        self.motorDriver.Stop()
                    elif (motor == 0):
                        self.motorDriver.Turn(self.PID())
                    else:
                        self.speed = self.Speed()
                        self.motorDriver.Drive(self.speed)
                elif (self.controlType == 1):
                    if (self.prevSteer != self.steeringM and motor == 0):
                        self.prevSteer = self.steeringM
                        if (self.steeringM == 2):
                            self.motorDriver.ManualLeft()
                        elif (self.steeringM == 1):      
                            self.motorDriver.ManualRight()
                        elif (self.steeringM == 0):
                            self.motorDriver.ManualSteerStop()
                    elif (self.prevDrive != self.drivingM and motor == 1):
                        self.prevDrive = self.drivingM
                        if (self.drivingM == 2):
                            self.motorDriver.ManualForward()
                        elif (self.drivingM == 1):
                            self.motorDriver.ManualReverse()
                        elif (self.drivingM  == 0):
                            self.motorDriver.ManualDriveStop()
            sleep(0.01)
    def StartCar(self):
        try:
            # creating thread
            t1 = threading.Thread(target=self.driveCar, args=(0,))
            t2 = threading.Thread(target=self.driveCar, args=(1,))

            # starting thread 1
            t1.start()
            # starting thread 2
            t2.start()
        except Exception as e:
            print(e)
            sys.exit(0)
