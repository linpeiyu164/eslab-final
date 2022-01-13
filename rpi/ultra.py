import RPi.GPIO as GPIO
import time
import threading
import rpi_car

# global dist1, dist2
# dist1 = 100
# dist2 = 100
def measure(TRIG, ECHO, i):
    global dist1
    global dist2
    while True:
       GPIO.output(TRIG, True)
       time.sleep(0.00001)
       GPIO.output(TRIG, False)
       while GPIO.input(ECHO)==0:
          pulse_start = time.time()
    
       while GPIO.input(ECHO)==1:
          pulse_end = time.time()
       pulse_duration = pulse_end - pulse_start
       distance = pulse_duration * 17150
       distance = round(distance+1.15, 2)
      # print("distance"+str(i)+" "+str(distance)+" cm")
      # dist = distance
       if i==1:
           dist1 = distance
       else:
           dist2 = distance
       time.sleep(1)
