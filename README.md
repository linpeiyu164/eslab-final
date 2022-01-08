# ESLab - HW2
Transmit sensor data to Linux host, code is based on mbed-os-example-sockets.
## Wireless connection
```sh
"nsapi.default-wifi-ssid": "\"SSID\"",
"nsapi.default-wifi-password": "\"PASSWORD\""
```
## Sensor transmission
The run() method in the SocketDemo class contains additional code for sensor data transmission.
## Socket server
```sh
python3 source/socket_server.py
```
The socket server runs locally on a host. The board must be under the same local network to be able to access the server through its local IP address (which is hard-coded as 192.168.1.9 at the moment).
To get local IP address : 
```sh
ipconfig getifaddr en0
```
- HOST : 0.0.0.0
- PORT : 8000

## Plotting
Use pygal to plot our acceleration chart. Three lines x, y, z will be plotted against a time length of 200 seconds. The output file will be saved in the current directory as chart.svg.
```sh
pip install pygal
```

