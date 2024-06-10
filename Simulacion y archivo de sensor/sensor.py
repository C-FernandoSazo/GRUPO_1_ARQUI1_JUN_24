import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)
sensor1 = 17  # Asumiendo que este es el GPIO para el sensor1
sensor2 = 18  # Asumiendo que este es el GPIO para el sensor2

GPIO.setup(sensor1, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(sensor2, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

# Variable para almacenar el estado de los sensores
estado_sensor1 = False
estado_sensor2 = False

def monitorizar_entrada_salida():
    global estado_sensor1, estado_sensor2
    try:
        while True:
            estado_actual_sensor1 = GPIO.input(sensor1)
            estado_actual_sensor2 = GPIO.input(sensor2)

            # Detecta la secuencia de entrada
            if estado_actual_sensor1 and not estado_sensor1:
                # Sensor 1 activado
                time.sleep(0.05)  # Pequeño delay para evitar rebotes
                if GPIO.input(sensor2):
                    print("Una persona ha entrado.")
                    estado_sensor1 = False  # Restablece el estado para la próxima detección

            # Detecta la secuencia de salida
            elif estado_actual_sensor2 and not estado_sensor2:
                # Sensor 2 activado
                time.sleep(0.05)  # Pequeño delay para evitar rebotes
                if GPIO.input(sensor1):
                    print("Una persona ha salido.")
                    estado_sensor2 = False  # Restablece el estado para la próxima detección

            # Actualiza los estados anteriores
            estado_sensor1 = estado_actual_sensor1
            estado_sensor2 = estado_actual_sensor2

            time.sleep(0.1)  # Pausa para evitar sobrecarga del CPU

    except KeyboardInterrupt:
        print("Interrupción por teclado")
        GPIO.cleanup()  # Limpieza de los pines GPIO

# Ejecutar la función
monitorizar_entrada_salida()
