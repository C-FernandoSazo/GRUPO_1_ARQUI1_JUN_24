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
Exterior = 38 
Area_Recepcion = 36
Area_Conferencia = 40
Area_Trabajo = 35
Area_Administracion = 37
Cafeteria = 24
Bano = 26
Area_Transporte = 22

GPIO.setup(sensor_exterior, GPIO.IN)

# Estado inicial
state = {
    "lights": {
        "Area_Recepcion": False,
        "Area_Conferencia": False,
        "Area_Trabajo": False,
        "Area_Administracion": False,
        "Cafeteria": False,
        "Area_Transporte": False,
        "Bano": False,
        "Exterior": False
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
                GPIO.output(Exterior, GPIO.LOW)
                state["lights"][Exterior] = False
            else:
                print("Es de noche, LED encendido")
                GPIO.output(Exterior, GPIO.HIGH)
                state["lights"][Exterior] = True
            sleep(1) 
    except KeyboardInterrupt:
        GPIO.cleanup()
        print("Programa interrumpido y GPIO limpio")



#Manejo de solicitudes

@app.route('/')
def home():
    return "Bienvenido a la API de control del establecimiento!"


#Luces
@app.route('/api/lights/<area>', methods=['POST'])
def toggle_light(area):
    if area in state["lights"]:
        state["lights"][area] = not state["lights"][area]
        try:
            if not state["lights"][area]:
                #Luz encendida
                lcd.message(f"Luz {area}: ON", 1)
                #GPIO.output(area, GPIO.HIGH)
                state["lights"][area] = True
            else: 
                #Luz apagada
                lcd.message(f"Luz {area}: OFF", 1)
                #GPIO.output(area, GPIO.LOW)
                state["lights"][area] = False
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
    

    if request.method == 'POST':
        state["isGateOpen"] = not state["isGateOpen"]
        print("SE ACCIONA")
        try:
            lcd.message("CONVEYOR", 1)
            lcd.message("  MOVING", 2)
        except KeyboardInterrupt:
            GPIO.cleanup()
        return jsonify({"success": True, "isConveyorMoving": state["isConveyorMoving"]}), 200
    elif request.method == 'GET':
        print("SE MUEVE")
        return jsonify({"isConveyorMoving": state["isConveyorMoving"]}), 200

@app.route('/api/gate', methods=['GET', 'POST'])
def handle_gate():
    if request.method == 'POST':
        state["isGateOpen"] = not state["isGateOpen"]
        print("SE ACCIONA")
        try:
            lcd.message("ABRIENDO", 1)
            lcd.message("PORTON", 2)
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
    lcd.message("<G1_ARQUI1>", 1)
    lcd.message("<VACAS_JUN_24>", 2)
    sleep(5)
