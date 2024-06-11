from flask import Flask, request, jsonify
import RPi.GPIO as GPIO
from time import sleep
import threading
from flask_cors import CORS
from flask_socketio import SocketIO, emit
from LCD import LCD

app = Flask(__name__)
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")

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

#Sensores
sensor1 = 11 
sensor2 = 12 

# Variable para almacenar el estado de los sensores
estado_sensor1 = False
estado_sensor2 = False
Entrada = False
Salida = False

personas = 0

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

pin_mapping = {
    "Exterior": 38,
    "Area_Recepcion": 36,
    "Area_Conferencia": 40,
    "Area_Trabajo": 35,
    "Area_Administracion": 37,
    "Cafeteria": 24,
    "Bano": 26,
    "Area_Transporte": 22
}

# Variable de control para pausar y reanudar el hilo
pause_thread = False

# Hilos

# Sensor de fotoresistencia exterior
def sensorExterior():
    global pause_thread
    try:
        while True:
            print(pause_thread)
            if not pause_thread:
                # Lee el estado del sensor de luz
                if GPIO.input(sensor_exterior):
                    print("Es de noche, LED encendido")
                    GPIO.output(Exterior, GPIO.HIGH)
                else:
                    print("Es de dia, LED apagado")
                    GPIO.output(Exterior, GPIO.LOW)
            sleep(1) 
    except KeyboardInterrupt:
        GPIO.cleanup()
        print("Programa interrumpido y GPIO limpio")

# Sensor digital
# Sensor digital
def monitorizar_entrada_salida():
    global estado_sensor1, estado_sensor2, Entrada, Salida, personas
    try:
        contador = 0
        while True:
            estado_actual_sensor1 = GPIO.input(sensor1)
            estado_actual_sensor2 = GPIO.input(sensor2)
            print("estados " + str(estado_actual_sensor1) + " " + str(estado_actual_sensor2))
            print(f"vals {Entrada} {Salida}")
            
            if contador == 20:
                Entrada = False
                Salida = False
                contador = 0

            if not estado_actual_sensor1 and estado_actual_sensor2:
                # Primer sensor activado y segundo inactivo
                Entrada = True
                Salida = False

            if estado_actual_sensor1 and not estado_actual_sensor2 and Entrada:
                # Segundo sensor activado después del primero
                print("Entro")
                personas += 1
                print(f"Personas: {personas}")
                increment_people_count()
                Entrada = False

            if estado_actual_sensor1 and not estado_actual_sensor2:
                # Segundo sensor activado y primero inactivo
                Salida = True
                Entrada = False

            if not estado_actual_sensor1 and estado_actual_sensor2 and Salida:
                # Primer sensor activado después del segundo
                print("Salio")
                personas -= 1
                print(f"Personas: {personas}")
                decrement_people_count()
                Salida = False
            contador += 1
            sleep(0.1)  # Pequeño delay para evitar sobrecarga del CPU y debouncing

    except KeyboardInterrupt:
        print("Interrupción por teclado")
        GPIO.cleanup()



# Manejo de solicitudes

@app.route('/')
def home():
    return "Bienvenido a la API de control del establecimiento!"

# Luces
@app.route('/api/lights/<area>', methods=['POST'])
def toggle_light(area):
    global pause_thread
    if area in state["lights"]:
        pin = pin_mapping[area]
        try:
            if not state["lights"][area]:
                # Luz encendida
                lcd.message(area, 1)
                lcd.message(f"Luz ON", 2)
                GPIO.output(pin, GPIO.HIGH)
                state["lights"][area] = True
                if area == "Exterior":
                    pause_thread = True  # Pausar el hilo
            else: 
                # Luz apagada
                lcd.message(area, 1)
                lcd.message(f"Luz OFF", 2)
                GPIO.output(pin, GPIO.LOW)
                state["lights"][area] = False
                if area == "Exterior":
                    pause_thread = False  # Reanudar el hilo
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

def increment_people_count():
    state["peopleCount"] += 1
    socketio.emit('update_people_count', {'peopleCount': state["peopleCount"]})

def decrement_people_count():
    global state
    if state["peopleCount"] > 0:
        state["peopleCount"] -= 1
    socketio.emit('update_people_count', {'peopleCount': state["peopleCount"]})


def setup():
    GPIO.setup(Exterior, GPIO.OUT)
    GPIO.setup(Area_Recepcion, GPIO.OUT)
    GPIO.setup(Area_Conferencia, GPIO.OUT)
    GPIO.setup(Area_Trabajo, GPIO.OUT)
    GPIO.setup(Area_Administracion, GPIO.OUT)
    GPIO.setup(Cafeteria, GPIO.OUT)
    GPIO.setup(Bano, GPIO.OUT)
    GPIO.setup(Area_Transporte, GPIO.OUT)
    GPIO.setup(sensor_exterior, GPIO.IN)
    GPIO.setup(sensor1, GPIO.IN)
    GPIO.setup(sensor2, GPIO.IN)

def cleanup_gpio():
    GPIO.cleanup()
    
if __name__ == '__main__':
    try:
        setup()
        lcd.message("<G1_ARQUI1>", 1)
        lcd.message("<VACAS_JUN_24>", 2)
        sleep(5)  
        #sensorExt = threading.Thread(target=sensorExterior)
        #sensorExt.start()
        sensorDigital = threading.Thread(target=monitorizar_entrada_salida)
        sensorDigital.start()
        socketio.run(app, debug=True)
 
    except KeyboardInterrupt:
        cleanup_gpio()
    finally:
        cleanup_gpio()
