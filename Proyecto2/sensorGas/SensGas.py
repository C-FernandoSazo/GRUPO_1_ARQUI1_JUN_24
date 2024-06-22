import RPi.GPIO as GPIO
import time

# Configuración de los pines GPIO
GPIO.setmode(GPIO.BCM)  # Usar numeración BCM
GPIO.setup(17, GPIO.IN)  # Configurar el pin 17 como entrada
calidad=[]
def leer_sensor_mq2():

    estado_sensor = GPIO.input(17)
    if estado_sensor == GPIO.LOW:
        print("Gas detectado!")
        calidad.append(1)
    else:
        print("No se detecta gas.")
        calidad.append(0)

try:
    while True:
        leer_sensor_mq2()
        print(calidad)
        time.sleep(1)  # Esperar 1 segundo antes de la siguiente lectura
except KeyboardInterrupt:
    print("Programa terminado")
finally:
    GPIO.cleanup()  # Limpiar la configuración de los pines GPIO