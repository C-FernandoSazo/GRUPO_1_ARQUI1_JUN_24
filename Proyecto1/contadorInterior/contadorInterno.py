import RPi.GPIO as GPIO
from time import sleep

# Configuración inicial de GPIO
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

# Definimos los puertos a utilizar para el decoder de BCD a decimal para el display y los sensores
# Siendo el BCD0 el bit menos significativo y BCD3 el bit más significativo
BCD0 = 12
BCD1 = 13
BCD2 = 15
BCD3 = 16
SensorEntrada = 7
SensorSalida = 11

# Forma en qué los GPIOS se van a comportar
GPIO.setup(BCD0, GPIO.OUT)
GPIO.setup(BCD1, GPIO.OUT)
GPIO.setup(BCD2, GPIO.OUT)
GPIO.setup(BCD3, GPIO.OUT)
GPIO.setup(SensorEntrada, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(SensorSalida, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

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

# Código principal
try:
    while True:
        if GPIO.input(SensorEntrada) and not GPIO.input(SensorSalida):
            NumPersonas += 1
            print("Persona entrando")
            esperar = True
            while esperar:  # Espera a que el sensor de entrada se desactive
                sleep(0.05)
                if GPIO.input(SensorSalida):
                    print("While entrada")
                    esperar = False
                    print("Entro")
        elif GPIO.input(SensorSalida) and not GPIO.input(SensorEntrada):
            NumPersonas -= 1
            print("Persona saliendo")
            esperar = True
            while esperar:  # Espera a que el sensor de entrada se desactive
                sleep(0.05)
                if GPIO.input(SensorEntrada):
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
