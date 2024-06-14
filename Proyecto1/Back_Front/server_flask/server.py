from flask import Flask, request, jsonify
import RPi.GPIO as GPIO
from time import sleep
import threading
from flask_cors import CORS
from flask_socketio import SocketIO, emit
from LCD import LCD
from queue import Queue

app = Flask(__name__)
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")

lcd = LCD(2, 0x27)

message_queue = Queue()
lcd_timer = threading.Timer(3.0, lambda: None)  

GPIO.setmode(GPIO.BOARD)  # Asegurando que el modo de numeración de pines se establece al inicio

# Sensor Fotorresistencia
sensor_exterior = 16

# Sensor Interior
BCD0 = 8
BCD1 = 10
BCD2 = 11
BCD3 = 13
SensorEntrada = 19
SensorSalida = 21

# Puertos 7 y 15 LIbres



# Leds
Exterior = 38 
Area_Recepcion = 36
Area_Conferencia = 40
Area_Trabajo = 35
Area_Administracion = 37
Cafeteria = 24
Bano = 26
Area_Transporte = 22

# Sensor Perimetral
BUZZER_PIN = 29
ldr_pin = 31

# Motor Banda
pinA = 16
pinB = 18
pinEnable = 12  
pwm1 = None

# Motor Garage
pin1 = 23
pin2 = 32
pinEna = 33
pwm2 = None

# Variable de control para pausar y reanudar el hilo
pause_thread = False
Entrada = False
Salida = False

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
    "personas": 0,
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

# Hilos

# Sensor de fotoresistencia exterior
def sensorExterior():
    global pause_thread
    try:
        while True:
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
                message_queue.put((area, "Luz ON"))
                GPIO.output(pin, GPIO.HIGH)
                state["lights"][area] = True
                if area == "Exterior":
                    pause_thread = True  # Pausar el hilo
            else: 
                # Luz apagada
                message_queue.put((area, "Luz OFF"))
                GPIO.output(pin, GPIO.LOW)
                state["lights"][area] = False
                if area == "Exterior":
                    pause_thread = False  # Reanudar el hilo
        except KeyboardInterrupt:
            GPIO.cleanup()
        return jsonify({"success": True, "lights": state["lights"]}), 200
    else:
        return jsonify({"error": "Area not found"}), 404


@app.route('/api/peopleCount', methods=['POST'])
def increment_people_count():
    state["peopleCount"] += 1
    return jsonify({"success": True, "peopleCount": state["peopleCount"]}), 200

@app.route('/api/gate', methods=['GET', 'POST'])
def handle_gate():
    if request.method == 'POST':
        state["isGateOpen"] = not state["isGateOpen"]
        print("SE ACCIONA")
        try:
            if not state["isGateOpen"]:
                message_queue.put(("Abriendo...", "Porton"))
                motor_adelante_porton(75) 
                sleep(5)
                detener_porton()
                state["isGateOpen"] = True
            else:
                message_queue.put(("Cerrando...", "Porton"))
                motor_atras_porton(75) 
                sleep(5)
                detener_porton()
                state["isGateOpen"] = False
        except KeyboardInterrupt:
            GPIO.cleanup()
        return jsonify({"success": True, "isGateOpen": state["isGateOpen"]}), 200
    elif request.method == 'GET':
        print("ESTA CERRADO")
        return jsonify({"isGateOpen": state["isGateOpen"]}), 200
        
@app.route('/api/conveyor', methods=['POST'])
def toggle_gate():
    if not state["isConveyorMoving"]:
        message_queue.put(("La banda", "esta girando"))
        motor_adelante_banda(75)
        state["isConveyorMoving"] = True
    else:
        message_queue.put(("La banda", "se detuvo"))
        detener_banda()
        state["isConveyorMoving"] = False
    
    # Devolver el estado actual de la puerta y si fue abierta o cerrada
    return jsonify({"success": True, "isGateOpen": state["isConveyorMoving"]})

# Sensor Perimetral
def alarmaPerimetral():
    try:
        while True:
            # Lee el estado del sensor de luz
            print("ciclo")
            if not GPIO.input(ldr_pin):
                print("Se detecto movimientos")
                state["isAlarmActive"] = True
                while True:
                    handle_sensor_activado()
                    GPIO.output(BUZZER_PIN, GPIO.HIGH)
                    sleep(10)
                    GPIO.output(BUZZER_PIN, GPIO.LOW)
                    sleep(1)
                    break
            else:
                handle_sensor_activado()
                print("No movimiento ")
                state["isAlarmActive"] = False
            sleep(0.5)
    except KeyboardInterrupt:
        GPIO.cleanup()
        print("Programa interrumpido y GPIO limpio")

# Motor Banda

def motor_adelante_banda(velocidad):
    global pwm1, pinA, pinB
    lcd.message("Abriendo...", 1)
    pwm1.ChangeDutyCycle(velocidad)
    GPIO.output(pinA, GPIO.HIGH)
    GPIO.output(pinB, GPIO.LOW)

def detener_banda():
    global pwm1, pinA, pinB
    lcd.message("Esperando...", 1)
    pwm1.ChangeDutyCycle(0)  # Motor apagado
    GPIO.output(pinA, GPIO.LOW)
    GPIO.output(pinB, GPIO.LOW)


# Motor Garage
def motor_adelante_porton(velocidad):
    global pwm2, pin1, pin2
    lcd.message("Abriendo...", 1)
    pwm2.ChangeDutyCycle(velocidad)
    GPIO.output(pin1, GPIO.HIGH)
    GPIO.output(pin2, GPIO.LOW)

def motor_atras_porton(velocidad):
    global pwm2, pin1, pin2
    lcd.message("Cerrando...", 1)
    pwm2.ChangeDutyCycle(velocidad)
    GPIO.output(pin1, GPIO.LOW)
    GPIO.output(pin2, GPIO.HIGH)

def detener_porton():
    global pwm2, pin1, pin2
    lcd.message("Esperando...", 1)
    pwm2.ChangeDutyCycle(0)  # Motor apagado
    GPIO.output(pin1, GPIO.LOW)
    GPIO.output(pin2, GPIO.LOW)

# Sensor Interior Display
# Variables
numerosBinario = [
    [0, 0, 0, 0],
    [0, 0, 0, 1],
    [0, 0, 1, 0],
    [0, 0, 1, 1],
    [0, 1, 0, 0],
    [0, 1, 0, 1],
    [0, 1, 1, 0],
    [0, 1, 1, 1],
    [1, 0, 0, 0],
    [1, 0, 0, 1]
]

# Funciones
def conversorDecimalBinario(numero):
    return numerosBinario[numero]

def asignacion(binario):
    GPIO.output(BCD0, binario[3])
    GPIO.output(BCD1, binario[2])
    GPIO.output(BCD2, binario[1])
    GPIO.output(BCD3, binario[0])
    
def sensorInterior():
    try:
        contador = 0
        while True:
            estado_actual_sensor1 = GPIO.input(SensorEntrada)
            estado_actual_sensor2 = GPIO.input(SensorSalida)
            print("estados " + str(estado_actual_sensor1) + " " + str(estado_actual_sensor2))

            if estado_actual_sensor1 and not estado_actual_sensor2:
                while True:
                    estado_actual_sensor2 = GPIO.input(SensorSalida)
                    if estado_actual_sensor2: 
                        print("Entro")
                        increment_people_count()
                        sumarNumero()
                        break
                    sleep(0.1)
                print("salio del while -----------------------------------------------------------------")

            sleep(0.5)
            if not estado_actual_sensor1 and estado_actual_sensor2:
                while True:
                    estado_actual_sensor1 = GPIO.input(SensorEntrada)
                    if estado_actual_sensor1: 
                        print("Salio")
                        restarNumero()
                        break
                    sleep(0.1)


        
            contador += 1
            sleep(1)  # Pequeño delay para evitar sobrecarga del CPU y debouncing

    except KeyboardInterrupt:
        print("Interrupción por teclado")
        GPIO.cleanup()
        
def sumarNumero():
    global state
    print(state["personas"])
    if state["personas"] < 9:
        state["personas"] += 1
        cadenaBinario = conversorDecimalBinario(state["personas"])
        asignacion(cadenaBinario)
    else:
        state["personas"] = 0
        cadenaBinario = conversorDecimalBinario(state["personas"])
        asignacion(cadenaBinario)

def restarNumero():
    global state
    print(state["personas"])
    if state["personas"] > 0:
        state["personas"] -= 1
        cadenaBinario = conversorDecimalBinario(state["personas"])
        asignacion(cadenaBinario)
    

def increment_people_count():
    state["peopleCount"] += 1
    socketio.emit('update_people_count', {'peopleCount': state["peopleCount"]})    

def handle_sensor_activado():
    socketio.emit('update_alarm_state', {'isAlarmActive': state["isAlarmActive"] })

def display_lcd():
    global lcd_timer
    while True:
        if not message_queue.empty() and not lcd_timer.is_alive():
            message = message_queue.get()
            lcd.message(message[0], 1)
            lcd.message(message[1], 2)
            lcd_timer = threading.Timer(3.0, lcd.clear)  # Establece el temporizador para borrar la pantalla después de 3 segundos
            lcd_timer.start()
        
def setup():

    global pwm1, pwm2  # Agregar esta línea para indicar que pwm es global
    # Pines de Leds
    GPIO.setup(Exterior, GPIO.OUT)
    GPIO.setup(Area_Recepcion, GPIO.OUT)
    GPIO.setup(Area_Conferencia, GPIO.OUT)
    GPIO.setup(Area_Trabajo, GPIO.OUT)
    GPIO.setup(Area_Administracion, GPIO.OUT)
    GPIO.setup(Cafeteria, GPIO.OUT)
    GPIO.setup(Bano, GPIO.OUT)
    GPIO.setup(Area_Transporte, GPIO.OUT)
    # Pin Sensor Exterior
    GPIO.setup(sensor_exterior, GPIO.IN)
    # Pines Sensor Perimetral
    GPIO.setup(BUZZER_PIN, GPIO.OUT)
    GPIO.setup(ldr_pin, GPIO.IN)
    # Pines Sensor Interior
    GPIO.setup(BCD0, GPIO.OUT)
    GPIO.setup(BCD1, GPIO.OUT)
    GPIO.setup(BCD2, GPIO.OUT)
    GPIO.setup(BCD3, GPIO.OUT)
    GPIO.setup(SensorEntrada, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(SensorSalida, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    # Pines Motor Banda
    GPIO.setup(pinA, GPIO.OUT)
    GPIO.setup(pinB, GPIO.OUT)
    GPIO.setup(pinEnable, GPIO.OUT)
    # Pines Motor Porton
    GPIO.setup(pin1, GPIO.OUT)
    GPIO.setup(pin2, GPIO.OUT)
    GPIO.setup(pinEna, GPIO.OUT)
    pwm1 = GPIO.PWM(pinEnable, 1000)  # Frecuencia de PWM de 1000 Hz
    pwm1.start(0)
    pwm2 = GPIO.PWM(pinEna, 1000)  # Frecuencia de PWM de 1000 Hz
    pwm2.start(0)


if __name__ == '__main__':
    try:
        setup()
        lcd.message("<G1_ARQUI1>", 1)
        lcd.message("<VACAS_JUN_24>", 2)
        sleep(10)
        lcd.clear()
        lcd_thread = threading.Thread(target=display_lcd)
        lcd_thread.start()
        hilo = threading.Thread(target=sensorInterior)
        hilo.start()
        hilo2= threading.Thread(target=alarmaPerimetral)
        hilo2.start()
        socketio.run(app, debug=True)
    except KeyboardInterrupt:
        GPIO.cleanup()
    finally:
        GPIO.cleanup()
