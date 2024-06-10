
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
sensor1 = 17  # Asumiendo que este es el GPIO para el sensor1
sensor2 = 18  # Asumiendo que este es el GPIO para el sensor2

GPIO.setup(sensor1, GPIO.IN)
GPIO.setup(sensor2, GPIO.IN)

# Variable para almacenar el estado de los sensores
estado_sensor1 = False
estado_sensor2 = False

def monitorizar_entrada_salida():
    global estado_sensor1, estado_sensor2
    try:
        while True:
            estado_actual_sensor1 = False
            estado_actual_sensor2 = False
            estado_actual_sensor1 = GPIO.input(sensor1)
            estado_actual_sensor2 = GPIO.input(sensor2)
            print("estados " + str(estado_actual_sensor1) +" "+ str(estado_actual_sensor2))
            # Detecta la secuencia de entrada
            if estado_actual_sensor1 and not estado_sensor1:
                # Sensor 1 activado
                time.sleep(0.1)  # Pequeño delay para evitar rebotes
                if GPIO.input(sensor2):
                    print("Una persona ha entrado.")
                    estado_sensor1 = False  # Restablece el estado para la próxima detección

            # Detecta la secuencia de salida
            elif estado_actual_sensor2 and not estado_sensor2:
                # Sensor 2 activado
                time.sleep(0.1)  # Pequeño delay para evitar rebotes
                if GPIO.input(sensor1):
                    print("Una persona ha salido.")
                    estado_sensor2 = False  # Restablece el estado para la próxima detección

            # Actualiza los estados anteriores
            estado_sensor1 = estado_actual_sensor1
            estado_sensor2 = estado_actual_sensor2

            time.sleep(0.2)  # Pausa para evitar sobrecarga del CPU

    except KeyboardInterrupt:
        print("Interrupcin por teclado")
        GPIO.cleanup()  # Limpieza de los pines GPIO

# Ejecutar la función
monitorizar_entrada_salida()
