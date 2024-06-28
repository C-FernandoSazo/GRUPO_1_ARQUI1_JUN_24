from flask import Flask, jsonify
import RPi.GPIO as GPIO
import random
from flask_cors import CORS
import threading
import time
import adafruit_dht
import board
import subprocess
from flask_socketio import SocketIO, emit
from bmp_280 import BMP280

app = Flask(__name__)
lock = threading.Lock()
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")
SENSOR_PIN = 5  
wind_count = 0
radius_cm = 1.0  # Radio del anemómetro en cm
wind_interval = 5  # Intervalo de tiempo para medir en segundos

bmp = BMP280(port=1, mode=BMP280.FORCED_MODE, oversampling_p=BMP280.OVERSAMPLING_P_x16, oversampling_t=BMP280.OVERSAMPLING_T_x1,
            filter=BMP280.IIR_FILTER_OFF, standby=BMP280.T_STANDBY_1000)

# Array global para almacenar los datos
global_data = []
humedad_data = []
calidad_data = []
wind_speeds = [] 
aire_data = []
presion_data = []

def luminucidad():
    try:
        while True:
            estado_sensor = GPIO.input(22)
            if estado_sensor == GPIO.LOW:
                calidad = "Soleado"
            else:
                calidad = "Nublado"
            print(f"Estado del sensor: {calidad}")
            socketio.emit('luminosidad', {'status': calidad})
            time.sleep(1)
    except KeyboardInterrupt:
        print("Programa terminado")
        
def leer_sensor_mq2():
    try:
        while True:
            estado_sensor = GPIO.input(17)
            if estado_sensor == GPIO.LOW:
                calidada = "Mala"
                aire_data.append(0)
            else:
                calidada = "Buena"
                aire_data.append(1)
            print(f"Calidad del aire: {calidada}")
            buena, mala = counter_air(aire_data)
            socketio.emit('calidad_aire', {'bueno': buena, 'malo': mala})
            time.sleep(5)
    except KeyboardInterrupt:
        print("Programa terminado")

# Cálculo de la velocidad del viento
def calculate_wind_speed(time_sec):
    global wind_count
    circumference_cm = 2 * 3.1416 * radius_cm  # Circunferencia del anemómetro
    rotations = wind_count / 2.0  # Cada pulso es medio ciclo (2 pulsos = 1 rotación completa)
    wind_speed_cm_sec = (circumference_cm * rotations) / time_sec
    wind_speed_km_h = (wind_speed_cm_sec / 100000) * 3600  # Convertir cm/s a km/h
    return wind_speed_km_h

def velocidad():
    try:
        global wind_count
        last_state = GPIO.input(SENSOR_PIN)
        start_time = time.time()
        while True:
            current_state = GPIO.input(SENSOR_PIN)
            if last_state == GPIO.HIGH and current_state == GPIO.LOW:
                wind_count += 1
            last_state = current_state

            if time.time() - start_time >= wind_interval:
                wind_speed = calculate_wind_speed(wind_interval)
                if wind_speed > 0:
                    velocidadd = round(wind_speed)
                    wind_speeds.append(velocidadd)
                    print(f"Velocidad del viento: {wind_speed:.2f} km/h")
                    time.sleep(5)  
                wind_count = 0  
                start_time = time.time()
    except KeyboardInterrupt:
        print("Medición terminada por el usuario")
        print("Velocidades registradas:", wind_speeds)
        
def barometro():
    pressure = bmp.read_pressure()
    while True:
        try:
            print("Pressure (hPa): " + str(pressure))
            data = round(pressure / 10)
            presion_data.append(data)
            time.sleep(5)
        except RuntimeError as e:
            print(f'Error al leer el barometro: {e}')

def fill_data():
    # Configura el sensor DHT11 en el pin GPIO 23
    dht_sensor = adafruit_dht.DHT11(board.D23)
    while True:
        try:
            temperatura = dht_sensor.temperature
            humedad = dht_sensor.humidity
            
            if temperatura is not None and humedad is not None:
                print(f'Temperatura: {temperatura:.1f}°C, Humedad: {humedad:.1f}%')
                global_data.append(temperatura)
                humedad_data.append(humedad)
            else:
                print('Fallo al leer los datos del sensor.')
            time.sleep(5)
        except RuntimeError as e:
            print(f'Error al leer el sensor DHT11: {e}')

def calculate_average(data):
    contenido = ','.join(map(str, data)) + '\n'
    with open("promedio.txt", "w") as archivo:
        archivo.write(contenido)
    path_al_ejecutable = "./promedio"

    result = subprocess.run([path_al_ejecutable], input=contenido, text=True, capture_output=True)
    
def mediana(data):
    input_data = ','.join(f"{x}" for x in data) + '\n'  # Convertir array a string
    result = subprocess.run(['./mediana'], input=input_data, text=True, capture_output=True)
    return result.returncode  # Convertir salida a entero
    
def maximo(data):
    input_data = ','.join(f"{x}" for x in data) + '\n'  # Convertir array a string
    result = subprocess.run(['./maximo'], input=input_data, text=True, capture_output=True)
    return result.returncode  # Convertir salida a entero

def minimo(data):
    input_data = ','.join(f"{x}" for x in data) + '\n'  # Convertir array a string
    result = subprocess.run(['./minimo'], input=input_data, text=True, capture_output=True)
    return result.returncode  # Convertir salida a entero
    
def desviacionest(data):
    contenido = ','.join(map(str, data)) + '\n'
    print(contenido)
    with open("desviacion.txt", "w") as archivo:
        archivo.write(contenido)
    path_al_ejecutable = "./desviacion"
    result = subprocess.run([path_al_ejecutable], input=contenido, text=True, capture_output=True)

def contador(data):
    input_data = ','.join(f"{x}" for x in data) + '\n'  # Convertir array a string
    result = subprocess.run(['./contador'], input=input_data, text=True, capture_output=True)
    return result.returncode  # Convertir salida a entero
    
def moda(data):
    input_data = ','.join(f"{x}" for x in data) + '\n'  # Convertir array a string
    result = subprocess.run(['./moda'], input=input_data, text=True, capture_output=True)
    return result.returncode  # Convertir salida a entero
    
def counter_air(array):
    input_data = ','.join(f"{x}" for x in array) + '\n'  # Convertir array a string
    print(input_data)
    result = subprocess.run(['./airbueno'], input=input_data, text=True, capture_output=True)
    result2 = subprocess.run(['./airbad'], input=input_data, text=True, capture_output=True)
    return result.returncode, result2.returncode 
            
@app.route('/data/<string:panel_id>')
def get_data(panel_id):
    if panel_id not in ['temp', 'hum', 'viento', 'lum', 'aire', 'pres']:
        return jsonify({"error": "Invalid panel ID"}), 404
    print("DESDE APP", global_data)
    if panel_id == "hum":
        calculate_average(humedad_data)
        with open("respromedio.txt", "r") as file:
            average = file.read() 
        median = mediana(humedad_data)
        cont = contador(humedad_data)
        desviacionest(humedad_data)
        with open("resdesviacion.txt", "r") as file:
            desvst = file.read()
        maxi = maximo(humedad_data)
        mini = minimo(humedad_data)
        mod = moda(humedad_data)
        data = {
            "count": cont,
            "average": average,
            "median": median,
            "stdDev": desvst,
            "max": maxi,
            "min": mini,
            "mode": mod
        }
        return jsonify(data)
    if panel_id == "temp":
        calculate_average(global_data)
        with open("respromedio.txt", "r") as file:
            average = file.read() 
        median = mediana(global_data)
        cont = contador(global_data)
        desviacionest(global_data)
        with open("resdesviacion.txt", "r") as file:
            desvst = file.read()
        maxi = maximo(global_data)
        mini = minimo(global_data)
        mod = moda(global_data)
        data = {
            "count": cont,
            "average": average,
            "median": median,
            "stdDev": desvst,
            "max": maxi,
            "min": mini,
            "mode": mod
        }
        return jsonify(data)
    if panel_id == "viento":
        print(wind_speeds)
        calculate_average(wind_speeds)
        with open("respromedio.txt", "r") as file:
            average = file.read() 
        median = mediana(wind_speeds)
        cont = contador(wind_speeds)
        desviacionest(wind_speeds)
        with open("resdesviacion.txt", "r") as file:
            desvst = file.read()
        maxi = maximo(wind_speeds)
        mini = minimo(wind_speeds)
        mod = moda(wind_speeds)                                            
        data = {
            "count": cont,
            "average": average,
            "median": median,
            "stdDev": desvst,
            "max": maxi,
            "min": mini,
            "mode": mod
        }
        return jsonify(data)
    if panel_id == "pres":
        print(presion_data)
        calculate_average(presion_data)
        with open("respromedio.txt", "r") as file:
            average = file.read() 
        median = mediana(presion_data)
        cont = contador(presion_data)
        desviacionest(presion_data)
        with open("resdesviacion.txt", "r") as file:
            desvst = file.read()
        maxi = maximo(presion_data)
        mini = minimo(presion_data)
        mod = moda(presion_data)                                            
        data = {
            "count": cont,
            "average": average,
            "median": median,
            "stdDev": desvst,
            "max": maxi,
            "min": mini,
            "mode": mod
        }
        return jsonify(data)
    
def setup():
    GPIO.setup(22, GPIO.IN)
    GPIO.setup(17, GPIO.IN)
    GPIO.setup(SENSOR_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

if __name__ == '__main__':
    setup()
    data_thread = threading.Thread(target=fill_data)
    data_thread.start()
    hilolumi = threading.Thread(target=luminucidad)
    hilolumi.start()
    hilo_mq2 = threading.Thread(target=leer_sensor_mq2)
    hilo_mq2.start()
    hilovel = threading.Thread(target=velocidad)
    hilovel.start()
    hilobar = threading.Thread(target=barometro)
    hilobar.start()
    socketio.run(app, debug=True, use_reloader = False)
