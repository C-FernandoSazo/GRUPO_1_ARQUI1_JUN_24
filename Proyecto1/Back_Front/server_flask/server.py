from flask import Flask, request, jsonify
import RPi.GPIO as GPIO
from time import sleep
import random
import threading
from flask_cors import CORS

from LCD import LCD

app = Flask(__name__)
CORS(app)

lcd = LCD(2,0x27) 

GPIO.setmode(GPIO.BOARD)

#Sensor Fotorresistencia
sensor_exterior = 16
#Leds
led_exterior = 38 
led_recepcion = 36
led_conferencia = 40
led_banda = 35
led_admin = 37
led_cafeteria = 24
led_bano = 26
led_garage = 22

GPIO.setup(sensor_exterior, GPIO.IN)

# Estado inicial
state = {
    "lights": {
        "led_recepcion": False,
        "led_conferencia": False,
        "led_banda": False,
        "led_admin": False,
        "led_cafeteria": False,
        "led_exterior": False,
        "led_bano": False,
        "led_garage": False
    },
    "peopleCount": 0,
    "isConveyorMoving": False,
    "isGateOpen": False,
    "isAlarmActive": False
}

#Hilos

#Sensor de fotoresistencia exterior

def sensorExterior():
    try:
        while True:
            # Lee el estado del sensor de luz
            if GPIO.input(sensor_exterior):
                print("Es de dia, LED apagado")
                GPIO.output(led_exterior, GPIO.LOW)
            else:
                print("Es de noche, LED encendido")
                GPIO.output(led_exterior, GPIO.HIGH)
            sleep(1) 
    except KeyboardInterrupt:
        GPIO.cleanup()
        print("Programa interrumpido y GPIO limpio")



#Manejo de solicitudes

@app.route('/')
def home():
    return "Bienvenido a la API de control del establecimiento!"

@app.route('/api/lights/<area>', methods=['POST'])
def toggle_light(area):
    if area in state["lights"]:
        state["lights"][area] = not state["lights"][area]
        try:
            lcd.message("Se encendio la luz de "+area, 1)
            
        except KeyboardInterrupt:
            GPIO.cleanup()
        return jsonify({"success": True, "lights": state["lights"]}), 200
    else:
        return jsonify({"error": "Area not found"}), 404

@app.route('/api/peopleCount', methods=['GET'])
def get_people_count():
    return jsonify({"peopleCount": state["peopleCount"]}), 200

@app.route('/api/peopleCount', methods=['POST'])
def increment_people_count():
    state["peopleCount"] += 1
    return jsonify({"success": True, "peopleCount": state["peopleCount"]}), 200

@app.route('/api/conveyor', methods=['POST'])
def toggle_conveyor():
    state["isConveyorMoving"] = not state["isConveyorMoving"]
    return jsonify({"success": True, "isConveyorMoving": state["isConveyorMoving"]}), 200

@app.route('/api/gate', methods=['GET', 'POST'])
def handle_gate():
    if request.method == 'POST':
        state["isGateOpen"] = not state["isGateOpen"]
        print("SE ACCIONA")
        try:
            lcd.message("Caracoles", 1)
        except KeyboardInterrupt:
            GPIO.cleanup()
        return jsonify({"success": True, "isGateOpen": state["isGateOpen"]}), 200
    elif request.method == 'GET':
        print("ESTA CERRADO")
        return jsonify({"isGateOpen": state["isGateOpen"]}), 200

@app.route('/api/alarm', methods=['POST'])
def toggle_alarm():
    state["isAlarmActive"] = not state["isAlarmActive"]
    return jsonify({"success": True, "isAlarmActive": state["isAlarmActive"]}), 200


if __name__ == '__main__':
    app.run(debug=True)
