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

#Sensor Interior
BCD0 = 8
BCD1 = 10
BCD2 = 11
BCD3 = 13
SensorEntrada = 19
SensorSalida = 21

#Sensor Digital
sensor1 = 7
sensor2 = 15

#Leds
Exterior = 38 
Area_Recepcion = 36
Area_Conferencia = 40
Area_Trabajo = 35
Area_Administracion = 37
Cafeteria = 24
Bano = 26
Area_Transporte = 22

#Sensor Perimetral
buzzer_pin = 29
ldr_pin = 31

#Motor Banda
pinA = 16
pinB = 18
pinEnable = 12  
pwm1 = None

#Motor Garage
pin1 = 23
pin2 = 32
pinEna = 33
pwm2 = None

# Variable de control para pausar y reanudar el hilo
pause_thread = False
Entrada = False
Salida = False
Entrada2 = False
Salida2 = False

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

#Hilos

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
def sensorDigital():
    global Entrada, Salida
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
                increment_people_count()
                Entrada = False

            if estado_actual_sensor1 and not estado_actual_sensor2:
                # Segundo sensor activado y primero inactivo
                Salida = True
                Entrada = False

            if not estado_actual_sensor1 and estado_actual_sensor2 and Salida:
                # Primer sensor activado después del segundo
                print("Salio")
                Salida = False
            contador += 1
            sleep(0.1)

    except KeyboardInterrupt:
        print("Interrupción por teclado")
        GPIO.cleanup()


#Manejo de solicitudes

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
                motor_adelante_porton(75) 
                sleep(5)
                detener_porton()
                state["isGateOpen"] = True
            else:
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
        motor_adelante_banda(75)
        state["isConveyorMoving"] = True
    else:
        detener_banda()
        state["isConveyorMoving"] = False
    
    # Devolver el estado actual de la puerta y si fue abierta o cerrada
    return jsonify({"success": True, "isGateOpen": state["isConveyorMoving"]})

#Sensor Perimetral
def toggle_alarm():
    try:
        while True:
            # Lee el estado del sensor de luz
            if GPIO.input(ldr_pin):
                buzz(1000,5)
                state["isAlarmActive"] = True
            else:
                state["isAlarmActive"] = False
            sleep(1) 
    except KeyboardInterrupt:
        GPIO.cleanup()
        print("Programa interrumpido y GPIO limpio")

def buzz(pitch, duration):
    period = 1.0 / pitch
    delay = period / 2
    cycles = int(duration * pitch)
    for i in range(cycles):
        GPIO.output(buzzer_pin, True)
        sleep(delay)
        GPIO.output(buzzer_pin, False)
        sleep(delay)


#Motor Banda

def motor_adelante_banda(velocidad):
    global pwm1, pinA, pinB
    lcd.message("Abriendo...",1)
    pwm1.ChangeDutyCycle(velocidad)  
    GPIO.output(pinA, GPIO.HIGH)
    GPIO.output(pinB, GPIO.LOW)

def detener_banda():
    global pwm1, pinA, pinB
    lcd.message("Esperando...",1)
    pwm1.ChangeDutyCycle(0)  # Motor apagado
    GPIO.output(pinA, GPIO.LOW)
    GPIO.output(pinB, GPIO.LOW)


#Motor Garage
def motor_adelante_porton(velocidad):
    global pwm2, pin1, pin2
    lcd.message("Abriendo...",1)
    pwm2.ChangeDutyCycle(velocidad)  
    GPIO.output(pin1, GPIO.HIGH)
    GPIO.output(pin2, GPIO.LOW)

def motor_atras_porton(velocidad):
    global pwm2, pin1, pin2
    lcd.message("Cerrando...",1)
    pwm2.ChangeDutyCycle(velocidad)
    GPIO.output(pin1, GPIO.LOW)
    GPIO.output(pin2, GPIO.HIGH)

def detener_porton():
    global pwm2, pin1, pin2
    lcd.message("Esperando...",1)
    pwm2.ChangeDutyCycle(0)  # Motor apagado
    GPIO.output(pin1, GPIO.LOW)
    GPIO.output(pin2, GPIO.LOW)

#Sensor Interior Display
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
    global Entrada2, Salida2
    try:
        contador = 0
        personas = 0
        while True:
            estado_actual_sensor1 = GPIO.input(sensor1)
            estado_actual_sensor2 = GPIO.input(sensor2)
            print("estados " + str(estado_actual_sensor1) + " " + str(estado_actual_sensor2))
            print(f"vals {Entrada2} {Salida2}")
            print(f"Personas: {personas}")
            
            if contador == 20:
                Entrada2 = False
                Salida2 = False
                contador = 0

            if not estado_actual_sensor1 and estado_actual_sensor2:
                # Primer sensor activado y segundo inactivo
                Entrada2 = True
                Salida2 = False

            if estado_actual_sensor1 and not estado_actual_sensor2 and Entrada2:
                # Segundo sensor activado después del primero
                print("Entro")
                if personas < 9:
                    personas += 1
                    print(f"Personas: {personas}")
                else:
                    lcd.message("Limite de", 1)
                    lcd.message("Personas 9", 2)
                Entrada2 = False

            if estado_actual_sensor1 and not estado_actual_sensor2:
                # Segundo sensor activado y primero inactivo
                Salida2 = True
                Entrada2 = False

            if not estado_actual_sensor1 and estado_actual_sensor2 and Salida2:
                # Primer sensor activado después del segundo
                print("Salio")
                if personas > 0:
                    personas -= 1
                    print(f"Personas: {personas}")
                else:
                    lcd.message("No hay", 1)
                    lcd.message("Personas", 2)
                Salida2 = False

            cadenaBinario = conversorDecimalBinario(personas)
            asignacion(cadenaBinario)
            contador += 1
            sleep(0.1)  # Pequeño delay para evitar sobrecarga del CPU y debouncing

    except KeyboardInterrupt:
        print("Interrupción por teclado")
        GPIO.cleanup()

def increment_people_count():
    state["peopleCount"] += 1
    socketio.emit('update_people_count', {'peopleCount': state["peopleCount"]})    
    
        
def setup():
    global pwm1, pwm2  # Agregar esta línea para indicar que pwm es global
    #Pines de Leds
    GPIO.setup(Exterior, GPIO.OUT)
    GPIO.setup(Area_Recepcion, GPIO.OUT)
    GPIO.setup(Area_Conferencia, GPIO.OUT)
    GPIO.setup(Area_Trabajo, GPIO.OUT)
    GPIO.setup(Area_Administracion, GPIO.OUT)
    GPIO.setup(Cafeteria, GPIO.OUT)
    GPIO.setup(Bano, GPIO.OUT)
    GPIO.setup(Area_Transporte, GPIO.OUT)
    #Pin Sensor Exterior
    GPIO.setup(sensor_exterior, GPIO.IN)
    #Pines Sensor Perimetral
    GPIO.setup(buzzer_pin, GPIO.OUT)
    GPIO.setup(ldr_pin, GPIO.IN)
    #Pines Sensor Digital
    GPIO.setup(sensor1, GPIO.IN)
    GPIO.setup(sensor2, GPIO.IN)
    #Pines Sensor Display
    GPIO.setup(BCD0, GPIO.OUT)
    GPIO.setup(BCD1, GPIO.OUT)
    GPIO.setup(BCD2, GPIO.OUT)
    GPIO.setup(BCD3, GPIO.OUT)
    GPIO.setup(SensorEntrada, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(SensorSalida, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    #Pines Motor Banda
    GPIO.setup(pinA, GPIO.OUT)
    GPIO.setup(pinB, GPIO.OUT)
    GPIO.setup(pinEnable, GPIO.OUT)
    #Pines Motor Porton
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
        sleep(5)
        lcd.clear()
        hilo = threading.Thread(target=sensorInterior)
        hilo.start()
        socketio.run(app, debug=True)
    except KeyboardInterrupt:
        GPIO.cleanup()
    finally:
        GPIO.cleanup()


