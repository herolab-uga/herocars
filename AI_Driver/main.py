import time
import getch
import socket
import threading
from flask import Flask, request,Response
import Controllers.CarController as CarController

car = CarController.CarController()

# Initialize web server for controlling the car
app = Flask("LGT_Car")

@app.route("/p", methods=["GET","POST"])
def p():
    if request.method == "GET":
       return str(car.p)
    else:
        car.p = int(request.form["data"])
        return Flask.Response(status=200)

@app.route("/i", methods=["GET","POST"])
def p():
    if request.method == "GET":
       return str(car.i)
    else:
        car.i = int(request.form["data"])
        return Flask.Response(status=200)

# Create route of /d 
@app.route("/d", methods=["GET","POST"])
def d():
    if request.method == "GET":
       return str(car.d)
    else:
        car.d = int(request.form["data"])
        return Flask.Response(status=200)

@app.route("/min_speed", methods=["GET","POST"])
def min_speed():
    if request.method == "GET":
       return str(car.min_speed)
    else:
        car.min_speed = int(request.form["data"])
        return Flask.Response(status=200)

@app.route("/max_speed", methods=["GET","POST"])
def max_speed():
    if request.method == "GET":
       return str(car.max_speed)
    else:
        car.max_speed = int(request.form["data"])
        return Flask.Response(status=200)

@app.route("/current_speed", methods=["GET"])
def current_speed():
    if request.method == "GET":
       return str(car.car_speed)

@app.route("/line_type", methods=["GET","POST"])
def line_type():
    if request.method == "GET":
       return str(car.line_type)
    else:
        car.line_type = int(request.form["data"])
        return Flask.Response(status=200)

@app.route("/control_type", methods=["GET","POST"])
def control_type():
    if request.method == "GET":
       return str(car.control_type)
    else:
        car.control_type = int(request.form["data"])
        return Flask.Response(status=200)

@app.route("/forward", methods=["GET"])
def min_speed():
    if request.method == "GET":
        car.last_velo_time = time.time()
        car.car_speed = car.max_speed
        car.drive_forward()
        return Flask.Response(status=200)

@app.route("/backward", methods=["GET"])
def backward():
    if request.method == "GET":
        car.last_velo_time = time.time()
        car.car_speed = -car.max_speed
        car.drive_backward()
        return Flask.Response(status=200)

@app.route("/left", methods=["GET"])
def min_speed():
    if request.method == "GET":
        car.last_steer_time = time.time()
        car.straight = 0
        car.turn_left()
        return Flask.Response(status=200)

@app.route("/right", methods=["GET"])
def min_speed():
    if request.method == "GET":
        car.last_steer_time = time.time()
        car.straight = 0
        car.turn_right()
        return Flask.Response(status=200)

if __name__ == '__main__':
    app.run("127.0.0.1", port=5000)


