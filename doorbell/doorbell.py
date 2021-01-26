# Time
from time import sleep
from datetime import datetime as dt
# to call bash file
from subprocess import check_output 
# Pins
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM) # Broadcom GPIO notation
GPIO.setwarnings(False)
# Random
import random as rd

# INPUTS
pinIn = 21 # the input pin

memes = [ # sound files
    'home/pi/doorbell/wavs/he_man.wav',
    'home/pi/doorbell/wavs/kazoo_who_ru.wav',
    'home/pi/doorbell/wavs/smithers_sitcom.wav',
    'home/pi/doorbell/wavs/maniscalco.wav',
    'home/pi/doorbell/wavs/signor_dingdong.wav',
    'home/pi/doorbell/wavs/windows95.wav'
]

def main():
    GPIO.setup(pinIn, GPIO.IN, GPIO.PUD_DOWN) # set input terminal with internal pull down resistor
    sleep(0.2) # don't take any imediate initial readings
    
    isHighLast = GPIO.input(pinIn)
    try:
        while True:
            if GPIO.input(pinIn):
                if not isHighLast: # changed to high
                    speaker_play()
                    isHighLast = True
                sleep(2)
            else:
                if isHighLast:     # changed to low
                    isHighLast = False
                sleep(0.46) # see pulses folder for derrivation
    except KeyboardInterrupt:
        print('Stopped')
    finally:
        GPIO.cleanup()
        print('cleaned up')

# turns on boom, connects to pi, then plays random meme
def speaker_play():
    print('Triggered at', dt.now().strftime('%d/%m/%Y, %H:%M:%S'))
    filePath = memes[rd.randint(0, len(memes)-1)]
    try:
        out = check_output('/home/pi/doorbell/play.sh ' + filePath, shell=True)
        for l in out.decode('utf-8').split('\n')[:-1]: print(' ', l)
        print('  Done')
    except Exception as e:
        print('WARNING: sound not played! Error is:', str(e))
  
main()
