# ESLab Final Project -- 看展覽車車
電機三 林霈瑀 張芯慈 王濰紳

## Introduction
![](https://i.imgur.com/1PqfZ0s.png)

## STM32
### Gesture Detection 
STM32 is able to detect the tilting movement of the board ex: forward, backward, left, right. The accelerator data is passed through a moving average filter. The data is then sent to RPI and Relay Server.

### Exhibit
We seperately place three STM32 board as exhibits, which possess ble service, and they will continuously broadcast bluetooth signals.

## RPI
### Car Control
RPI gets the instruction from STM32 ex: forward, backward, left, right. The rear wheel then move backward if RPI gets the instruction "backward" and move forward otherwise where as the front wheel steers right if RPI geta the instruction "right" and steers left if RPI gets the instruction "left".
### Exhibit Detection
Our car would periodically detect the nearest exhibit (or there's no exhibit nearby) using RSSI value. Record the one with the largest RSSI value, consider seven consecutive results and take the mode of them as final result for stability.

### Pi Camera

Video is streamed from the Pi camera to the relay server. 

We use the following gstreamer command :

```
gst-launch-1.0 -v v4l2src device="/dev/video0" ! videoconvert ! clockoverlay ! \
videoscale ! video/x-raw,width=640, height=360 !  x264enc bitrate=256 ! video/x-h264,profile=\"high\" ! \
mpegtsmux ! hlssink playlist-root=http://192.168.0.156:8080 location=segment_%05d.ts target-duration=1 max-files=10 playlist-length=1
```
The HLS protocol is used.This protocol allows us to stream the video on a web browser. We have noticed a delay due to the encoder and the playlist-length x target-duration. Current delay is about 1 second. 


## Relay Server

The relay server is between the STM32 board and the RPI car. The relay server has a frontend that displays the video footage from the RPI car and related information, such as current car motion and the nearest exhibit's introduction. 

## How to use
- ### STM32
1. Run stm32/exhibit.cpp on three STM32 boards, change the device name to Button1-3, respectively. 
 
```
const static char DEVICE_NAME[] = "Button3";
```

2. Run stm32/main.cpp on another STM32 for gesture detection.

- ### Relay Server
1. Run server/app.py on your laptop
2. Find the IPv4 address(192.168.X.X) of your laptop, and go to port 5000 (192.168.X.X:5000) on the browser to enter the website.

- ### RPi
1. Modify the IP address in ble.py and rpi_car.py in rpi folder, then run the codes
2. Run camera.sh

- ### RPi(run on boot)
    add the code below into /etc/rc.local before exit 0
    ```
    sudo /home/pi/eslabfinal/rpi/camera/camera.sh &
    sudo service bluetooth start &
    sleep 13s
    sudo python3 /home/pi/eslabfinal/rpi/ble.py &
    sudo python3 /home/pi/eslabfinal/rpi/rpi_car.py
    ```


## Future Prospects

* **Real-time streaming** : WebRTC could provide better real time streaming than HLS.
* **Remote access** : The current project can only be run under LAN, but remote access would be needed in practical situations.


