import RPi.GPIO as GPIO
import time

# Configuración del GPIO
SENSOR_PIN = 5  # GPIO 17 se corresponde con el pin físico 11 en la Raspberry Pi
GPIO.setmode(GPIO.BCM)
GPIO.setup(SENSOR_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Variables para la medición
wind_count = 0
radius_cm = 1.0  # Radio del anemómetro en cm
wind_interval = 5  # Intervalo de tiempo para medir en segundos
last_state = GPIO.input(SENSOR_PIN)

# Cálculo de la velocidad del viento
def calculate_wind_speed(time_sec):
    global wind_count
    circumference_cm = 2 * 3.1416 * radius_cm  # Circunferencia del anemómetro
    rotations = wind_count / 2.0  # Cada pulso es medio ciclo (2 pulsos = 1 rotación completa)
    wind_speed_cm_sec = (circumference_cm * rotations) / time_sec
    wind_speed_km_h = (wind_speed_cm_sec / 100000) * 3600  # Convertir cm/s a km/h
    return wind_speed_km_h

try:
    start_time = time.time()
    while True:
        current_state = GPIO.input(SENSOR_PIN)
        if last_state == GPIO.HIGH and current_state == GPIO.LOW:
            wind_count += 1
        last_state = current_state

        if time.time() - start_time >= wind_interval:
            wind_speed = calculate_wind_speed(wind_interval)
            print(f"Velocidad del viento: {wind_speed:.2f} km/h")
            wind_count = 0  # Reiniciar el contador
            start_time = time.time()

except KeyboardInterrupt:
    print("Medición terminada por el usuario")

finally:
    GPIO.cleanup()



