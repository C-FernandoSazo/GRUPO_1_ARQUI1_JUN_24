import adafruit_dht
import board
import time

# Configura el sensor DHT11 en el pin GPIO 23
dht_sensor = adafruit_dht.DHT11(board.D23)

while True:
    try:
        temperatura = dht_sensor.temperature
        humedad = dht_sensor.humidity
        
        if temperatura is not None and humedad is not None:
            print(f'Temperatura: {temperatura:.1f}°C, Humedad: {humedad:.1f}%')
        else:
            print('Fallo al leer los datos del sensor.')

    except RuntimeError as e:
        print(f'Error al leer el sensor DHT11: {e}')

    time.sleep(2)


    


