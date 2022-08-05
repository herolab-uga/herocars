import enum
import sys
import time
import getch
import socket
from flask_cors import CORS
from flask_socketio import SocketIO
from flask import Flask, request, Response, render_template, session
import AI_Driver.Controllers.CarController as CarController
# import jyserver.Flask as jsf

car = CarController.CarController()

# Initialize web server for controlling the car
app = Flask(__name__)
CORS(app)
socketio = SocketIO(app)

# @jsf.use(app)
# class App:
#     def __init__(self):
#         self.ids = ["ll","lm","mm","rm","rr"]

#     def update_ir(self):
#         line_state = [1,2,3,4,5]
#         # line_state = car.get_line_state()
#         for sensor,index in enumerate(line_state):
#             self.js.document.getElementById(self.ids[index]).innerHTML = "test"

# needs test
@app.route("/min_speed", methods=["POST"])
def min_speed():
    if request.method == "POST":
        todo = request.form.get("todo")
        car.min_speed = int(todo)
        # print("Minimum speed: " , todo)
    return App.render(render_template('index.html'))

# needs test
@app.route("/max_speed", methods=["POST"])
def max_speed():
    if request.method == "POST":
        todo = request.form.get("todo")
        car.max_speed = int(todo)
        # print("Maximum speed: " , todo)
    return App.render(render_template('index.html'))

# needs to be added
@app.route("/current_speed", methods=["GET"])
def current_speed():
    if request.method == "GET":
       return str(car.car_speed)

# needs fix
@app.route("/controltype", methods=["POST"]) 
def control_type():
    if request.method == "POST":
        todo = request.form.get("todo")
        # print(todo)
        car.control_type = todo
    return App.render(render_template('index.html'))

@app.route("/forward")
def forward():
    car.last_velo_time = time.time()
    car.car_speed = car.max_speed
    car.drive_forward()
    return App.render(render_template('index.html'))

@app.route("/backward")
def backward():
    car.last_velo_time = time.time()
    car.car_speed = -car.max_speed
    car.drive_backward()
    return App.render(render_template('index.html'))

@app.route("/left")
def left():
    car.last_steer_time = time.time()
    car.straight = 0
    car.turn_left()
    return App.render(render_template('index.html'))

@app.route("/right")
def right():
    car.last_steer_time = time.time()
    car.straight = 0
    car.turn_right()
    return App.render(render_template('index.html'))

@app.route("/stop")
def stop():
    car.stop()
    return App.render(render_template('index.html'))

@app.route("/center_steering")
def center_steering():
    car.center_steering()
    return ("nothing")

@app.route("/linetype", methods=["POST"])
def linetype():
    if request.method == "POST":
        todo = request.form.get("todo")
        car.line_color = todo
    return App.render(render_template('index.html'))

@app.route("/p", methods=["POST"])
def set_p():
    if request.method == "POST":
        todo = request.form.get("todo")
        # print(todo)
        car.p = todo
    return App.render(render_template('index.html'))

@app.route("/i", methods=["POST"])
def set_i():
    if request.method == "POST":
        todo = request.form.get("todo")
        # print("I " ,todo)
        car.i = todo
    return App.render(render_template('index.html'))

@app.route("/d", methods=["POST"])
def set_d():
    if request.method == "POST":
        todo = request.form.get("todo")
        # print("D ", todo)
        car.d = todo
    return App.render(render_template('index.html'))

@app.route("/camera_feed")
def camera_feed():
    return Response(car.get_frame(),mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route("/irsensors",methods=["POST"])
def irsensors():
    print(session)
    # return render_template('index.html',irlist=car.get_line_state())
    return App.render(render_template('index.html'))

@app.route("/")
def execute():
    return App.render(render_template('index.html'))

@socketio.on('disconnect')
def test_disconnect():
    car.stop()
    car.center_steering()

if __name__ == '__main__':
    host_addr = socket.gethostbyname(socket.gethostname() + ".local")
    app.run(host_addr, port=8080)


