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

#Sensor Interior
BCD0 = 8
BCD1 = 10
BCD2 = 11
BCD3 = 13
SensorEntrada = 19
SensorSalida = 21


#Leds
Exterior = 38 
Area_Recepcion = 36
Area_Conferencia = 40
Area_Trabajo = 35
Area_Administracion = 37
Cafeteria = 24
Bano = 26
Area_Transporte = 22
buzzer_pin = 29
ldr_pin = 31
pinA = 16
pinB = 18
pinEnable = 12  

pwm = None

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
        
@app.route('/api/conveyor', methods=['POST'])
def toggle_gate():
    
    if not state["isConveyorMoving"]:
        motor_adelante(75)
        state["isConveyorMoving"] = True
    else:
        motor_detener()
        state["isConveyorMoving"] = False
    
    # Devolver el estado actual de la puerta y si fue abierta o cerrada
    return jsonify({"success": True, "isGateOpen": state["isConveyorMoving"]})

def toggle_alarm():
    state["isAlarmActive"] = not state["isAlarmActive"]
   
    
    period = 10  


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
        

def motor_adelante(velocidad):
    global pwm, pinA, pinB
    lcd.message("Abriendo...",1)
    pwm.ChangeDutyCycle(velocidad)  # Ajusta la velocidad (ciclo de trabajo del PWM)
    GPIO.output(pinA, GPIO.HIGH)
    GPIO.output(pinB, GPIO.LOW)

def motor_atras(velocidad):
    global pwm, pinA, pinB
    lcd.message("Cerrando...",1)
    pwm.ChangeDutyCycle(velocidad)
    GPIO.output(pinA, GPIO.LOW)
    GPIO.output(pinB, GPIO.HIGH)

def motor_detener():
    global pwm, pinA, pinB
    lcd.message("Esperando...",1)
    pwm.ChangeDutyCycle(0)  # Motor apagado
    GPIO.output(pinA, GPIO.LOW)
    GPIO.output(pinB, GPIO.LOW)

def moverMotor():
    try:
        while True:
            print("MOviendo motor")
            motor_adelante(50)  # Motor hacia adelante a 50% de velocidad
            time.sleep(5)
            motor_detener()
            time.sleep(3)
            motor_atras(75)  # Motor hacia atrás a 75% de velocidad
            time.sleep(5)
            motor_detener()
            time.sleep(5)
    except KeyboardInterrupt:
        pwm.stop()  # Detiene el PWM
        GPIO.cleanup()  # Limpia la configuración del GPIO al salir
        

# Forma en qué los GPIOS se van a comportar


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
NumPersonas = 0
esperar = False

# Funciones
def conversorDecimalBinario(numero):
    return numerosBinario[numero]

def asignacion(binario):
    GPIO.output(BCD0, binario[3])
    GPIO.output(BCD1, binario[2])
    GPIO.output(BCD2, binario[1])
    GPIO.output(BCD3, binario[0])
    
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
            cadenaBinario = conversorDecimalBinario(personas)
            contador += 1
            sleep(0.1)  # Pequeño delay para evitar sobrecarga del CPU y debouncing

    except KeyboardInterrupt:
        print("Interrupción por teclado")
        GPIO.cleanup()


def sensorInterior():
    try:
        global numerosBinario, NumPersonas, esperar
        while True:
            if not GPIO.input(SensorEntrada) and GPIO.input(SensorSalida):
                NumPersonas += 1
                print("Persona entrando")
                esperar = True
                while esperar:  # Espera a que el sensor de entrada se desactive
                    sleep(0.05)
                    print("Entro a esperar")
                    if not GPIO.input(SensorSalida):
                        print("While entrada")
                        esperar = False
                        print("Entro")
            elif not GPIO.input(SensorSalida) and GPIO.input(SensorEntrada):
                NumPersonas -= 1
                print("Persona saliendo")
                esperar = True
                while esperar:  # Espera a que el sensor de entrada se desactive
                    sleep(0.05)
                    if not GPIO.input(SensorEntrada):
                        esperar = False
                        print("While salida")
                        print("Salio")
            
            NumPersonas = max(0, NumPersonas)  # Evita que el conteo sea negativo    
            print(f"La cantidad de personas dentro de la sucursal es: {NumPersonas}")

            cadenaBinario = conversorDecimalBinario(NumPersonas)
            asignacion(cadenaBinario)
            sleep(1)

    except KeyboardInterrupt:
        GPIO.cleanup()
    
    
        
def setup():
    global pwm  # Agregar esta línea para indicar que pwm es global
    GPIO.setup(buzzer_pin, GPIO.OUT)
    GPIO.setup(ldr_pin, GPIO.IN)
    GPIO.setup(BCD0, GPIO.OUT)
    GPIO.setup(BCD1, GPIO.OUT)
    GPIO.setup(BCD2, GPIO.OUT)
    GPIO.setup(BCD3, GPIO.OUT)
    GPIO.setup(SensorEntrada, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(SensorSalida, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(pinA, GPIO.OUT)
    GPIO.setup(pinB, GPIO.OUT)
    GPIO.setup(pinEnable, GPIO.OUT)
    pwm = GPIO.PWM(pinEnable, 1000)  # Frecuencia de PWM de 1000 Hz
    pwm.start(0)



if __name__ == '__main__':
    setup()
    lcd.message("<G1_ARQUI1>", 1)
    lcd.message("<VACAS_JUN_24>", 2)
    sleep(5)
    lcd.clear()
    hilo = threading.Thread(target=monitorizar_entrada_salida)
    hilo.start()
    app.run(debug=True)


