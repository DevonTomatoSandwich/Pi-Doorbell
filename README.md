# Pi Doorbell

Plays memes whenever someone rings the doorbell !

# How

Using python, a raspberry pi intercepts the transmition from a doorbell 
and will play a sound through a BLE (Bluetooth Low Energy) Speaker.

## Method 

When the doorbell button is pressed a signal is sent from the doorbell's transmitter to the doorbell's receiver. 
The reciever has a signal pin that outputs voltage when the doorbell rings. By connecting the receiver's signal pin to 
one of the raspberry pi's (3B+) GPIO pins, the pi can intercept the signal. 

When this signal is detected the BLE speaker is turned on (if not already on) which is possible due to BLE. 
Turning the speaker on is achieved by bluetooth snooping the params in the signal sent from the Boom app. 
The speaker is connected using bluetoothctl commands (if previously paired manually)
Then a meme (as a wav file) is chosen at random from a list of wav files and played using bluealsa's aplay command. 

The pi is powered by 5V from the wall, the reciever is powered by the 3V3 pin on the pi and the doorbell's transmitter is powered by its own battery.  

# Instructions

## install
  ### todo
## run
  ### todo
# issues
  ### todo
