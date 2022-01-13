"""
    *need to get rpi's IP address*
    1. /control: receive STM32 gesture (camera, direction)
    2. /controlrpi: send camera, direction order to rpi_server
    3. /info: receive nearest ble device from rpi_server ({"name":"Exibit k"})
    4. /listen: post Exibit info to website
"""
from flask import Flask, request, render_template, Response, redirect
from flask_cors import CORS
from gevent import monkey
import requests

import json
import time
import ast

app = Flask(__name__)
cors = CORS(app)

class Data:
    camera = ''
    direction = ''
    name = ''
    info = ''

data = Data()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/listen")
def listen():
    def respond_to_client():
        toggle = 0
        while True:
            global data
            _data = json.dumps({
                "camera" : data.camera, 
                "direction" : data.direction, 
                "name" : data.name, 
                "info" : data.info
            })
            time.sleep(0.1)
            toggle = not toggle
            yield f"id: 1\ndata: {_data}\nevent: online\n\n"
    return Response(respond_to_client(), mimetype='text/event-stream')

@app.route("/control", methods=['GET','POST'])
def control():
    # post data to mongo db
    global data
    info = {
        "Exhibit1" : "This is info for exhibit1",
        "Exhibit2" : "This is info for exhibit2",
        "Exhibit3" : "This is info for exhibit3",
        "Exhibit4" : "No nearby"
    }
    req_byte = request.data
    req_str = req_byte.decode("UTF-8")
    req_dict = ast.literal_eval(req_str)
    print(req_dict)
    #data.camera = req_dict["camera"]
    data.direction = req_dict["direction"]
    #print(data.camera, data.direction)
    # control_data = json.dumps({
    #     "camera" : data.camera, 
    #     "direction" : data.direction
    # })
    control_data = json.dumps({"direction" : data.direction})
    control_res = requests.post('http://192.168.0.156:3000/controlrpi', json=control_data)
    #print(control_res.status_code)
    if control_res.status_code==500:
        print("Error")
    exb_res = requests.get('http://192.168.0.156:3000/exb')
    exb_dict = exb_res.json()
    data.name = exb_dict["name"]
    data.info = info[data.name]
    return redirect('/listen')

"""
@app.route("/info", methods=['POST'])
def info():
    global data
    info = {
        "Exhibit1" : "This is info for exhibit1",
        "Exhibit2" : "This is info for exhibit2",
        "Exhibit3" : "This is info for exhibit3",
        "Exhibit4" : "This is info for exhibit4",
        "Exhibit5" : "This is info for exhibit5",
        "Exhibit6" : "This is info for exhibit6",
    }
    req_byte = request.data
    req_str = req_byte.decode("UTF-8")
    req_dict = ast.literal_eval(req_str)
    print(req_dict)
    data.name = req_dict["name"]
    data.info = info.get(data.name)
    return redirect('/listen')
"""

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
    http_server = WSGIServer(("0.0.0.0", 80), app)
    http_server.serve_forever()

