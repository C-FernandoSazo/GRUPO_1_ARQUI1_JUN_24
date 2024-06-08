import RPi.GPIO as GPIO
from time import sleep
import random

from LCD import LCD

lcd = LCD(2,0x27) 
# params available for rPi revision, I2C Address, and backlight on/off
# lcd = LCD(2, 0x3F, True)
#lcd_2 = LCD(2,0x22) 

GPIO.setmode(GPIO.BOARD)

try:
   while True:
      lcd.message("LUZ AREA TRABAJO: ON", 1)
      sleep(2)
      lcd.message("LUZ AREA RECEPCION: OFF", 1)
      sleep(2)
      lcd.message("<G1_ARQUI1>", 1)
      lcd.message("<VACAS_JUN_24>", 2)
      sleep(10)
      lcd.clear()
	
except KeyboardInterrupt:
      GPIO.cleanup()