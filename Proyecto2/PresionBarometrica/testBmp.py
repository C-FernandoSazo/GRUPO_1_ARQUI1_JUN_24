#--------------------------------------
# Modified from: https://github.com/kitflix/raspberrypi-iot-codes/blob/master/BMP180%20Sensor/testBmp.py
#--------------------------------------

import bmpsensor
import time
while True:
    temp, pressure, altitude = bmpsensor.readBmp180()
    tempC = temp
    tempF = (tempC * 1.8) + 32

    print("Temp in C:  ",tempC)
    print("Temp in F:  ",tempF)
    print("Pressure: ",pressure)
    print("Altitude: ",altitude)
    print("\n")
    
    time.sleep(5)
