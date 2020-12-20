# Pi Homecoming

Plays memes whenever someone comes home !

# How

Using python, a raspberry pi detects whenever certain ips join a wifi network 
and will play a sound through a BLE (Bluetooth Low Energy) Speaker.

## Method 
Every 10 seconds the pi pings each device using arping up to 10 times, each time with a 1 second deadline to respond. 
If device is found it is checked against previously found devices to see if it has joined since the last check.
If the device has joined since the last check, the BLE speaker is turned on (if not already on) which is possible due to BLE. 
Turning the speaker on is achieved by bluetooth snooping the params in the signal sent from the Boom app. 
The speaker is connected using bluetoothctl commands (if previously paired manually)
Then a wav file (depending on who joined) is played using bluealsa's aplay command. 
If two devices connect in the same check, only the first device sound is played (which could be changed easily)
If someone arrives to an empty house the sound is played (which could easily be changed)

# Instructions

## install
  ### todo
## run
  ### todo
# issues
  ### todo
