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
    img = ''

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
                "info" : data.info,
                "img":data.img
            })
            time.sleep(0.1)
            toggle = not toggle
            yield f"id: 1\ndata: {_data}\nevent: online\n\n"
    return Response(respond_to_client(), mimetype='text/event-stream')

@app.route("/direction", methods=['POST'])
def direction():
    global data
    req_byte = request.data
    req_str = req_byte.decode("UTF-8")
    direction_dict = ast.literal_eval(req_str)
    data.direction = direction_dict["direction"]
    return Response(status=200)

@app.route("/control", methods=['GET','POST'])
def control():
    # post data to mongo db
    global data
    info = {
        "Exhibit1" : "超級害羞的白熊，專長是畫畫，興趣是喝茶。因為北方實在太寒冷，剛好他又非常怕冷，所以毅然收拾包袱逃往南方。應對寒冷的方法就是用包袱巾包著自己。",
        "Exhibit2" : "吃完炸豬排的時候，盤子裡總剩下外層肥肉、脆脆，炸豬排就是這些剩餘食物的組合體。炸豬排身體有超過99%為麵團，剩下1%為豬肉，對自己是「賣剩的」感到很沒自信，順帶一提，炸豬排點上醬汁，將會非常美味。",
        "Exhibit3" : "與河童(?)不一樣，他是一隻真正的企鵝，經常環遊世界。直到一次到北方旅行時遇見了白熊，告訴白熊男方有溫暖的海洋，白熊因而離開北方，踏上了離鄉背井的旅途。",
        "Exhibit4" : "No nearby"
    }
    name = {
        "Exhibit1" : "白熊",
        "Exhibit2" : "炸豬排",
        "Exhibit3" : "企鵝",
        "Exhibit4" : "No nearby"
    }
    images = {
        "Exhibit1" : "1.png",
        "Exhibit2" : "2.png",
        "Exhibit3" : "3.png",
        "Exhibit4" : "No nearby"
    }
    req_byte = request.data
    req_str = req_byte.decode("UTF-8")
    exb_dict = ast.literal_eval(req_str)
    print(exb_dict)
   
    data.name = name[exb_dict["name"]]
    data.info = info[exb_dict["name"]]
    data.img = images[exb_dict["name"]]
    return Response(status=200)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
    http_server = WSGIServer(("0.0.0.0", 80), app)
    http_server.serve_forever()

