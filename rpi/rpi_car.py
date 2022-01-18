"""
    *need to get laptop's IP address* 192.168.43.144:5000
    1. /controlrpi: receive camera, direction order from app.py
    2. call carcontrol.py and control the car according to direction orders. *always call shutdown* 
"""

from flask import Flask, request, Response
from flask_cors import CORS
import RPi.GPIO as GPIO
from http.server import HTTPServer, SimpleHTTPRequestHandler, test
import sys
import threading
import json
import carcontrol
import hlsserver
import requests
import time

car = carcontrol.CarController()
car.shutdown()

app = Flask(__name__)
CORS(app)

class Data:
    camera = ''
    direction = ''
    name = ''
    info = ''

data = Data()

current_direction = ""
mutex = threading.Lock()

thd3 = threading.Thread(target=lambda: test(hlsserver.CORSRequestHandler, HTTPServer, port=int(sys.argv[1]) if len(sys.argv) > 1 else 8080))
thd3.start()

@app.route("/controlrpi", methods=['POST'])
def index():
    global current_direction
    input_json = request.get_json(force=True)

    if input_json:
        if "direction" in input_json:
            car.get = True
            data.direction = input_json.get("direction")
            mutex.acquire()
            current_direction = data.direction
            mutex.release()
        else:
            car.get = False
        if "camera" in input_json:
            data.camera = input_json.get("camera")
    print(data.direction)
    car.get_command(data.direction)
    return Response(status=200)

@app.route("/exb", methods=['GET'])
def info():
    print(request)
    f = open('/home/pi/eslabfinal/rpi/output.txt', 'r+')
    num = f.read()
    li = ['1','2','3']
    if num not in li:
        num = '4'
    info_dict = {"name": "Exhibit"+num}
    return json.dumps(info_dict)

def sendDirection():
    while(True):
        global current_direction
        mutex.acquire()
        info_dict = { "direction" : current_direction }
        mutex.release()
        res = requests.post('http://192.168.0.131:5000/direction', json=info_dict)
        time.sleep(0.1)

if __name__ == '__main__':
    threading.Thread(target=lambda: app.run(host="0.0.0.0", port=3000, debug=True, use_reloader=False)).start()
    thd4 = threading.Thread(target = sendDirection())
    thd4.start()