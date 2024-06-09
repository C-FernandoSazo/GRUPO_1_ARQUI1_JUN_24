from flask import Flask, request, jsonify
import RPi.GPIO as GPIO
from time import sleep
import random
from flask_cors import CORS

from LCD import LCD


app = Flask(__name__)
CORS(app)

lcd = LCD(2,0x27) 
# params available for rPi revision, I2C Address, and backlight on/off
# lcd = LCD(2, 0x3F, True)
#lcd_2 = LCD(2,0x22) 

GPIO.setmode(GPIO.BOARD)

# Estado inicial
state = {
    "lights": {
        "lobby": False,
        "warehouse": False,
        "exterior": False,
        "offices": False
    },
    "peopleCount": 0,
    "isConveyorMoving": False,
    "isGateOpen": False,
    "isAlarmActive": False
}

@app.route('/')
def home():
    return "Bienvenido a la API de control del establecimiento!"

@app.route('/api/lights/<area>', methods=['POST'])
def toggle_light(area):
    if area in state["lights"]:
        state["lights"][area] = not state["lights"][area]
        try:
            lcd.message("Zancudo", 1)
            
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
