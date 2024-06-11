from flask import Flask, request, jsonify
import RPi.GPIO as GPIO
from time import sleep
import random
import threading
from flask_cors import CORS
import time

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
        
        try:
            if not state["lights"][area]:
               
                lcd.message(area, 1)
                lcd.message(f"Luz ON", 2)
              
                state["lights"][area] = True
            else: 
                
                lcd.message(area, 1)
                lcd.message(f"Luz OFF", 2)
                
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
   
    
    buzzer_pin = 21
    ldr_pin = 20
    period = 10  

  
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(buzzer_pin, GPIO.OUT)
    GPIO.setup(ldr_pin, GPIO.IN)

    is_buzzing = False
    was_buzzing = False

    def buzz():
        GPIO.output(buzzer_pin, GPIO.HIGH)

    def stop_buzz():
        GPIO.output(buzzer_pin, GPIO.LOW)

    start_time = None

    try:
        while True:
            sensor_value = GPIO.input(ldr_pin)
            print(f"Valor del sensor LDR: {sensor_value}")
            time.sleep(0.5)

            if sensor_value == 0:  
                if not is_buzzing and not was_buzzing:
                    buzz()
                    start_time = time.time()
                    is_buzzing = True
                    was_buzzing = True
                    return jsonify({"success": True, "isAlarmActive": state["isAlarmActive"]}), 200


            if is_buzzing and (time.time() - start_time >= period):
                stop_buzz()
                is_buzzing = False
                return jsonify({"success": False, "isAlarmActive": state["isAlarmActive"]}), 200
                

            
            if sensor_value == 1 and not is_buzzing:
                was_buzzing = False

    except KeyboardInterrupt:
        GPIO.cleanup()



if __name__ == '__main__':
    app.run(debug=True)
    lcd.message("<G1_ARQUI1>", 1)
    lcd.message("<VACAS_JUN_24>", 2)
    sleep(5)


