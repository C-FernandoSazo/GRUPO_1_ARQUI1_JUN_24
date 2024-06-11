import RPi.GPIO as GPIO
from time import sleep

#pin 11 raspb
servo_pin=11


GPIO.setmode(GPIO.BOARD)

# Habilitar GPIO como salida
GPIO.setup(servo_pin,GPIO.OUT)

#PWM
servo1 = GPIO.PWM(servo_pin,50) 

#Los grados se manejan de 2-12

#Funcion 0 grados
def grado_0():
    servo1.ChangeDutyCycle(2)
    sleep(0.5)
    servo1.ChangeDutyCycle(0)

#Funcion 90 grados
def grado_90():
    servo1.ChangeDutyCycle(7.5)
    sleep(0.5)
    servo1.ChangeDutyCycle(0)

try:
    servo1.start(0)
    sleep(4)
    print('Llengo a 0 grados')
    grado_0()
    sleep(4)
    print('0 grados de nuevo')
    grado_0()
    sleep(4)
    print('Llendo a 90 grados')
    grado_90()
    sleep(4)
    print('Regresando a 0 grados')
    grado_0()
    servo1.stop()
    GPIO.cleanup()
except KeyboardInterrupt:
    GPIO.cleanup()