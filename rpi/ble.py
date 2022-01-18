from bluepy.btle import Peripheral, UUID
from bluepy.btle import Scanner, DefaultDelegate
import binascii
import time
from flask import Flask, request, Response
from flask_cors import CORS
import RPi.GPIO as GPIO
from http.server import HTTPServer, SimpleHTTPRequestHandler, test
import sys
import threading
import json
import hlsserver
import requests
from statistics import mode

BUTTON_SERVICE_UUID = 0xA000
BUTTON_STATE_CHARACTERISTIC_UUID = 0xA001
                                      

class ScanDelegate(DefaultDelegate):
    def __init__(self):
        DefaultDelegate.__init__(self)
    
#global num
path = 'output.txt'
num = 1
cur = 0
fst = True
while (1):
    scanner = Scanner().withDelegate(ScanDelegate())
    devices = scanner.scan(2.0)
    print("Scanning...")
    MAC = ["c4:19:1e:f4:e0:81", "d8:94:7e:7b:0b:6a", "d7:97:21:71:53:27"]
    RSSI = [-999, -999, -999]
    found = 0
    for dev in devices:
        if (found == 3):
            break
        elif dev.addr in MAC:
            n = MAC.index(dev.addr)
            print( "Button %s, RSSI = %d dB" %((n+1), dev.rssi))
            RSSI[n] = dev.rssi
            found += 1
    nearest = max(RSSI)
    num = RSSI.index(nearest)+1
    if not fst:
        ls[cur] = num
        cur = (cur+1)%7
    else:
        ls = [num for i in range(7)]
        fst = False
    num_m = mode(ls)
    print(ls)
    print(num_m)
    info_dict = {"name": "Exhibit"+str(num_m)}
    res = requests.post('http://192.168.0.131:5000/control', json=info_dict)
    # f = open(path, 'w')
    # f.write(str(num))
    if nearest > -999:
        print("nearest device: Button %d, RSSI = %d" %(num_m, nearest))
    else:
        print ("no nearby device")

        
    