import sys
import time
import getch
import socket
from flask_cors import COR
from flask import Flask, request, Response, render_template
import Controllers.CarController as CarController

car = CarController.CarController()

# Initialize web server for controlling the car
app = Flask("LTG_Car")
CORS(app)

@app.route("/p", methods=["GET","POST"])
def p():
    if request.method == "GET":
       return str(car.p)
    else:
        print(request.data)
        car.p = int(request.form["data"])
        return Flask.Response(status=200)

@app.route("/i", methods=["GET","POST"])
def i():
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

@app.route("/forward")
def forward():
    print("forward",file=sys.stderr)
    car.last_velo_time = time.time()
    car.car_speed = car.max_speed
    car.drive_forward()

@app.route("/backward")
def backward():
    print("backward")
    car.last_velo_time = time.time()
    car.car_speed = -car.max_speed
    car.drive_backward()

@app.route("/left")
def left():
    print("left")
    car.last_steer_time = time.time()
    car.straight = 0
    car.turn_left()

@app.route("/right")
def right():
    print("right")
    car.last_steer_time = time.time()
    car.straight = 0
    car.turn_right()

@app.route("/camera_frame", methods=["GET"])
def camera_frame():
    if request.method == "GET":
        return car.camera_frame["frame"]

@app.route("/")
def execute():
    return render_template("../index.html")

if __name__ == '__main__':
    app.run("127.0.0.1", port=5000)


