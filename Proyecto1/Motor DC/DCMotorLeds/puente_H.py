import RPi.GPIO as GPIO
from time import sleep
#motordc
ena = 15			
in1 = 16
in2 = 18

#LED rojo
LEDR= 22


GPIO.setmode(GPIO.BOARD)

#habilitar como salida
GPIO.setup(ena,GPIO.OUT)
GPIO.setup(in1, GPIO.OUT)
GPIO.setup(in2, GPIO.OUT)
GPIO.setup(LEDR,GPIO.OUT)

#PWM para controlar la velocidad
pwm_a = GPIO.PWM(ena,500)



def  Prender_Motor():
	GPIO.output(in1,False)
	GPIO.output(in2,True) #Usar esta salida para el led verde 
	GPIO.output(LEDR,False)#Para apagar led rojo cuando se prende el motor
	pwm_a.ChangeDutyCycle(50)#Velocidad del motor

#se puede usar al inicializar el sistema para tener el led rojo prendido desde el inicio
def Parar_Motor():
	GPIO.output(in1,False)
	GPIO.output(in2,False)
	GPIO.output(LEDR,True)#prende el led rojo
	pwm_a.stop()


try:
	#inicializar PWM
	pwm_a.start(0)
	Parar_Motor()
	sleep(2)
	print('A Favor del Reloj')
	Prender_Motor()
	i=0
	while i<4:
		sleep(3)
		print(i)
		i+=1
	Parar_Motor()
	sleep(10)
	GPIO.cleanup()
except KeyboardInterrupt:
	GPIO.cleanup()



