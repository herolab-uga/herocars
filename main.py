import sys
import time
import getch
import socket
from flask_cors import CORS
from flask_socketio import SocketIO
from flask import Flask, request, Response, render_template
import AI_Driver.Controllers.CarController as CarController

car = CarController.CarController()

# Initialize web server for controlling the car
app = Flask("LTG_Car")
CORS(app)
socketio = SocketIO(app)

# @app.route("/p", methods=["GET","POST"])
# def p():
#     if request.method == "GET":
#        return str(car.p)
#     else:
#         print(request.data)
#         car.p = int(request.form["data"])
#         print(car.p)
#         return Flask.Response(status=200)

# @app.route("/i", methods=["GET","POST"])
# def i():
#     if request.method == "GET":
#        return str(car.i)
#     else:
#         car.i = int(request.form["data"])
#         print(car.i)
#         return Flask.Response(status=200)

# # Create route of /d 
# @app.route("/d", methods=["GET","POST"])
# def d():
#     if request.method == "GET":
#        return str(car.d)
#     else:
#         car.d = int(request.form["data"])
#         print(car.d)
#         return Flask.Response(status=200)

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

@app.route("/control_type", methods=["GET","POST"])
def control_type():
    if request.method == "GET":
       return str(car.control_type)
    else:
        car.control_type = int(request.form["data"])
        return Flask.Response(status=200)

@app.route("/forward")
def forward():
    # car.last_velo_time = time.time()
    # car.car_speed = car.max_speed
    car.drive_forward()
    return ("nothing")

@app.route("/backward")
def backward():
    # car.last_velo_time = time.time()
    # car.car_speed = -car.max_speed
    car.drive_backward()
    return ("nothing")

@app.route("/left")
def left():
    # car.last_steer_time = time.time()
    # car.straight = 0
    car.turn_left()
    return ("nothing")

@app.route("/right")
def right():
    # car.last_steer_time = time.time()
    # car.straight = 0
    car.turn_right()
    return ("nothing")

@app.route("/stop")
def stop():
    car.stop()
    return ("nothing")

@app.route("/center_steering")
def center_steering():
    car.center_steering()
    return ("nothing")

@app.route("/0")
def set_white():
    car.line_color = "white"
    return ("nothing")

@app.route("/1")
def set_black():
    car.line_color = "black"
    return ("nothing")

@app.route("/p")
def set_p():
    print(request.data)
    car.p = int(request.form["data"])
    print(car.p)
    return Flask.Response(status=200)

@app.route("/i")
def set_i():
    print(request.data)
    car.i = int(request.form["data"])
    print(car.i)
    return Flask.Response(status=200)

@app.route("/d")
def set_d():
    print(request)
    car.d = int(request.form["d"])
    print(car.d)
    return Flask.Response(status=200)

@app.route("/camera_frame", methods=["GET"])
def camera_frame():
    if request.method == "GET":
        return car.camera_frame["frame"]

@app.route("/")
def execute():
    return render_template("index.html")

@socketio.on('disconnect')
def test_disconnect():
    car.stop()
    car.center_steering()

if __name__ == '__main__':
    host_addr = socket.gethostbyname(socket.gethostname() + ".local")
    app.run(host_addr, port=8080)


