import time # Time
# Bluetooth
import os, sys # to get current directory for reading a meme's .wav
import subprocess
import pexpect
# Pins
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM) # Broadcom GPIO notation
GPIO.setwarnings(False)
# Random
import random as rd

# INPUTS
pinIn = 21 # the input pin
memes = [ # sound files
    'wavs/he_man.wav',
    'wavs/kazoo_who_ru.wav',
    'wavs/smithers_sitcom.wav'
]
boomHex    = 'C0:28:8D:F4:4C:01' # the address of the boom speaker. Obtained with command: hcitool con
boomValue  = '5C5181FEE5AC01'    # the value of the boom speaker. Obtained with BT snoop and adding 01 at end
boomHandle = '0x0003'            # the handle of the boom speaker. Obtained with BT snoop

def main():
    GPIO.setup(pinIn, GPIO.IN, GPIO.PUD_DOWN) # set input terminal
    time.sleep(0.1) # to ensure pull down resistance setup and pin ready to read 
    isHighLast = GPIO.input(pinIn) # should give False as pull down resistance
    try:
        while True:
            if GPIO.input(pinIn):
                if not isHighLast: # changed to high
                    isHighLast = True
                    speaker_play()
                time.sleep(3)
            else:
                if isHighLast:     # changed to low
                    isHighLast = False
                time.sleep(0.1)
    except KeyboardInterrupt:
        print('Stopped')
    finally:
        GPIO.cleanup()
        print('cleaned up')

# turns on boom, connects to pi, then plays random meme
def speaker_play():
    randIndex = rd.randint(0, len(memes)-1)
    
    if speaker_on():
        if speaker_connect():
            filePath = os.path.join(sys.path[0], memes[randIndex])
            onCommand = 'aplay -D bluealsa:DEV=' + boomHex + ',PROFILE=a2dp ' + filePath
            try:
                subprocess.check_output(onCommand, shell=True)
            except Exception as e:
                print('WARNING: sound not played! Error is:', str(e))

# turns on boom
def speaker_on():
    try:
        onCommand = 'sudo gatttool -i hci0 -b ' + boomHex + ' --char-write-req -a '\
        + boomHandle + ' -n ' + boomValue
        subprocess.check_output(onCommand, shell=True)
        print('Speaker turned on!')
        return True
    except Exception as e:
        print('WARNING: Speaker not turned on! Error is:', str(e))
        return False

# connects to pi
def speaker_connect():
    iAttempt = 0
    while iAttempt < 5:
        # send connection signal from rpi
        btApp = pexpect.spawn('bluetoothctl', echo=True)
        btApp.send('connect ' + boomHex + '\n')
        time.sleep(1) # sleep for a bit to give the boom time to connect
        # check devices connected to rpi
        for l in subprocess.getoutput('hcitool con').split('\n\t> '):
            if boomHex in l.split(' '):
                print('Speaker connected!')
                return True
        iAttempt += 1 # if this attempt failed
        print(' not connected after', iAttempt, 'attempt(s).')
    print('WARNING: sound not played as BT never connected in 5 attempts')
    return False

main()