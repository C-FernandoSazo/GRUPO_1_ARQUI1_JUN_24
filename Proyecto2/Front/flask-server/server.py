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

app = Flask(__name__)
lock = threading.Lock()
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")

# Array global para almacenar los datos
global_data = []
humedad_data = []
calidad_data = []

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
            time.sleep(3)
    except KeyboardInterrupt:
        print("Programa terminado")
        
def leer_sensor_mq2():
    try:
        while True:
            estado_sensor = GPIO.input(17)
            if estado_sensor == GPIO.LOW:
                calidada = "Mala"
            else:
                calidada = "Buena"
            print(f"Calidad del aire: {calidada}")
            socketio.emit('calidad_aire', {'quality': calidada})
            time.sleep(4)
    except KeyboardInterrupt:
        print("Programa terminado")

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
    print("desde promedio: ",data)
    input_data = ','.join(f"{x}" for x in data) + '\n'  # Convertir array a string
    result = subprocess.run(['./promedio'], input=input_data, text=True, capture_output=True)
    return result.returncode  # Convertir salida a entero
    
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
    input_data = ','.join(f"{x}" for x in data) + '\n'  # Convertir array a string
    result = subprocess.run(['./desviacion'], input=input_data, text=True, capture_output=True)
    return result.returncode  # Convertir salida a entero

def contador(data):
    input_data = ','.join(f"{x}" for x in data) + '\n'  # Convertir array a string
    result = subprocess.run(['./contador'], input=input_data, text=True, capture_output=True)
    return result.returncode  # Convertir salida a entero
    
def moda(data):
    input_data = ','.join(f"{x}" for x in data) + '\n'  # Convertir array a string
    result = subprocess.run(['./moda'], input=input_data, text=True, capture_output=True)
    return result.returncode  # Convertir salida a entero
            
@app.route('/data/<string:panel_id>')
def get_data(panel_id):
    if panel_id not in ['temp', 'hum', 'viento', 'lum', 'aire', 'pres']:
        return jsonify({"error": "Invalid panel ID"}), 404
    print("DESDE APP", global_data)
    if panel_id == "hum":
        average = calculate_average(humedad_data)  # Pasar global_data a la función
        median = mediana(humedad_data)
        cont = contador(humedad_data)
        desvst = desviacionest(humedad_data)
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
    average = calculate_average(global_data)  # Pasar global_data a la función
    median = mediana(global_data)
    cont = contador(global_data)
    desvst = desviacionest(global_data)
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
    
def setup():
    GPIO.setup(22, GPIO.IN)
    GPIO.setup(17, GPIO.IN)

if __name__ == '__main__':
    setup()
    data_thread = threading.Thread(target=fill_data)
    data_thread.start()
    hilolumi = threading.Thread(target=luminucidad)
    hilolumi.start()
    hilo_mq2 = threading.Thread(target=leer_sensor_mq2)
    hilo_mq2.start()
    socketio.run(app, debug=True, use_reloader = False)
