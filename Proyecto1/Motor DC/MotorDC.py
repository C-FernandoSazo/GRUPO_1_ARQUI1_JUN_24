import RPi.GPIO as GPIO
import time

# Configuración de los pines del GPIO
GPIO.setmode(GPIO.BOARD)
pinA = 16
pinB = 18
pinEnable = 12  # Pin de habilitación del puente H

GPIO.setup(pinA, GPIO.OUT)
GPIO.setup(pinB, GPIO.OUT)
GPIO.setup(pinEnable, GPIO.OUT)

# Configuración de PWM en el pin de habilitación
pwm = GPIO.PWM(pinEnable, 157000)  # Frecuencia de PWM de 1000 Hz
pwm.start(0)  # Inicia PWM con 0% de ciclo de trabajo (motor apagado)

def motor_adelante(velocidad):
    pwm.ChangeDutyCycle(velocidad)  # Ajusta la velocidad (ciclo de trabajo del PWM)
    GPIO.output(pinA, GPIO.HIGH)
    GPIO.output(pinB, GPIO.LOW)

def motor_atras(velocidad):
    pwm.ChangeDutyCycle(velocidad)
    GPIO.output(pinA, GPIO.LOW)
    GPIO.output(pinB, GPIO.HIGH)

def motor_detener():
    pwm.ChangeDutyCycle(0)  # Motor apagado
    GPIO.output(pinA, GPIO.LOW)
    GPIO.output(pinB, GPIO.LOW)

try:
    while True:
        print("Girando")
        motor_adelante(50)  # Motor hacia adelante a 50% de velocidad
        time.sleep(5)
        motor_detener()
        time.sleep(1)
        motor_atras(75)  # Motor hacia atrás a 75% de velocidad
        time.sleep(2)
        motor_detener()
        time.sleep(1)
except KeyboardInterrupt:
    pwm.stop()  # Detiene el PWM
    GPIO.cleanup()  # Limpia la configuración del GPIO al salir
