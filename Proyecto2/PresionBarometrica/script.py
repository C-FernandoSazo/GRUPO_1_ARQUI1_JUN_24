import time
import datetime
import paho.mqtt.client as mqtt
import ssl
import json
import _thread

import bmpsensor
 
def on_connect(client, userdata, flags, rc):
    print("Connected to AWS IoT: " + str(rc))

client = mqtt.Client()
client.on_connect = on_connect
client.tls_set(ca_certs='./rootCA.pem', certfile='./certificate.pem.crt', keyfile='./private.pem.key', tls_version=ssl.PROTOCOL_SSLv23)
client.tls_insecure_set(True)
client.connect("Your_IoT_Endpoint", 8883, 60)

def publishData(msg):
    print(msg)
     
    while (True):
        temp, pressure, altitude = bmpsensor.readBmp180()
        tempC = temp
        tempF = (tempC * 1.8) + 32

        print("Temp in C:  ",tempC)
        print("Temp in F:  ",tempF)
        print("Pressure: ",pressure)
        print("")
        
        timestamp = datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S")

        client.publish("raspi/data", payload=json.dumps({"timestamp": timestamp, "tempC": tempC, "tempF": tempF, "pressure": pressure}), qos=0, retain=False)

        time.sleep(300)
 
_thread.start_new_thread(publishData,("Spin-up new Thread...",))

client.loop_forever()
