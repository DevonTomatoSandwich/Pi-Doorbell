# Pi Doorbell

Plays memes whenever someone rings the doorbell !

```diff
- IMPORTANT The tune that comes with the doorbell will always be triggered 
- BUT bluetooth will not always connect so not 100% consistent. 
```

A Raspberry Pi intercepts the receiver signal from a doorbell transmission
and, using python, will play a greeting sound (a meme) through a BLE (Bluetooth Low Energy) Speaker.

# Components

- BLE Speaker: using Ultimate Ears Boom3 (~200AUD) for this project
- Doorbell: HPM Wireless Doorbell Kit model D642/01 (~10AUD)
- Raspberry Pi: model 3B+ with 5V charger and noobs (~100AUD)
- 3 gpio leads, each with alligator clip to female end (~10AUD)

Total cost is ~320AUD

Luckily I have a boom3 and pi so this project cost me $20

# Wiring Pics
Picture below shows the wiring of the pi to the receiver

![link1](readme_pics/wiring_photo_v3.jpg)

Main components can be shown in the below schematic 

![link2](readme_pics/wiring_shematic_v3.png)

## Overview 

When the doorbell button is pressed a signal is sent from the doorbell's transmitter to the doorbell's receiver. 
The receiver has a LED cathode wire that pulses when the doorbell rings. By connecting the receiver's LED to 
one of the raspberry Pi's GPIO pins, the Pi can intercept the signal. 

The Pi's python script "doorbell.py" listens for the signal on its GPIO pin. When detected it will run the bash script "play.sh" which 
 - turns the speaker on (if not already on), which is possible due to BLE.  
 - connects to the Boom using bluetoothctl commands (if previously paired and trusted manually)
 - chooses a meme (as a wav file) at random from a list of wav files and plays it using pulseaudio's paplay command. 

The pi is powered by 5V from the wall, the receiver is powered by the 3V3 pin on the pi and the doorbell's transmitter is powered by its own battery.  

# Instructions

## install

- Install Raspberry Pi OS with desktop with debian: (release: 10, codename: buster) the December 4 update
- Use the instructions from [the December update](https://www.raspberrypi.org/blog/new-raspberry-pi-os-release-december-2020/) under section "How do I get it?" to properly configure pulseaudio and remove bluealsa

- Download this repo as a zip.
- In the existing /home/pi folder of your pi insert the 'doorbell' folder found in the repo.
- Ensure file permissions are ok on scripts and logs
  - doorbell.py and play.sh scripts must be executable so run  
    `chmod a+x doorbell/doorbell.py`  
    `chmod a+x doorbell/play.sh`
  - also the log file must be writeable so run  
    `chmod a+w doorbell/doorbell.log`
- (optional) add other wav files of your choosing ensuring to match the uploaded file names with the file names in the memes array at the top of 'doorbell.py'.
- Setup the .py script to run on boot using systemd. For this project you need to:
  - run the below command in a terminal  
    `sudo nano /etc/systemd/user/doorbell.service`  
    Note that the user directory is important as pulse audio only plays from a user and not a root user.
    This [archlinux wiki](https://wiki.archlinux.org/index.php/Systemd/User) has other directories where systemd 
    will specifically start user services (which includes /etc/systemd/user/)
  - paste the code below into the file
    ```
    [Unit]
    Description=Plays memes whenever someone rings the doorbell
    After=bluetooth.target

    [Service]
    ExecStart=/bin/bash -c '/usr/bin/python3 -u /home/pi/doorbell/doorbell.py > /home/pi/doorbell/doorbell.log 2>&1'
    ExecStop=sudo pkill -9 -f doorbell/doorbell.py

    [Install]
    WantedBy=default.target
    ```
    The .service file will start on boot after the bluetooth unit is finished.
    The ExecStart command runs the doorbell.py python script with the -u tag so stdout is captured. 
    The stdout is moved to doorbell.log which tracks all logs since service start. 
    2>&1 also ensures errors are printed in the logs.
  - to save,  
    hit: ctrl + x, y, enter  
    and run the following commands  
    `sudo systemctl daemon-reload`  
    `systemctl --user enable doorbell.service`
  
## bluetooth

Information about hacking a Boom3 can be found in [this reddit post](https://www.reddit.com/r/shortcuts/comments/dz9zun/finally_turn_on_ue_boom_bluetooth_speaker/). 
To summarise the post:

Download the Ultimate ears app and connect to the Boom3 device. The app has a button that turns the Boom3 on. This feature is possible as the device is BLE.
The aim is to sniff the package sent to the boom to find its handle, value and device hex. However as pointed out in the comments there are easier ways to find these variables.
 - handle: for a boom3 the handle will be '0x0003'. For other BLE speakers or even the megaboom this may be different and you may need to sniff packets like in the post either with Packetlogger or Wireshark (I used wireshark for android).
 - value: this is just an address appended with '01' where the address is the bluetooth address of the phone which has the ultimate ears app installed. find BT address [for ios](https://www.techwalla.com/articles/how-do-i-find-a-bluetooth-address) or [for android](https://www.technipages.com/android-find-bluetooth-address). Note that while running the doorbell project the ultimate ears app has no effect on the bluetooth functionality. In other words the phone does not need to be awake or even on. The address is only needed to trick the boom into thinking the phone is turning it on when really the signal is being fabricated by the Pi. 
 - device hex: if you manually connect the pi to the boom3, and run `hcitool con` you can see a list of devices connected to the pi. Only connecting the boom3 should show one hex address corresponding to the boom3

You should now replace the variables `BOOM_HEX`, `BOOM_VALUE`, `BOOM_HANDLE` in the "play.sh" script.

"play.sh" also has `BOOM_CARD` which may be needed in the rare case where the device is connected but not sinked. To get this card value, you must pair and trust the boom manually with the Pi. Then run  
`pacmd list-cards`  
Each card has a unique variable called "index" which is aligned leftmost. You may see cards for an audio jack and hdmi but find the card that contains the boom's hex. Under the index, copy the contents of the name field inside and excluding the arrow <> brackets, and set this as the `BOOM_CARD`

"play.sh" also has absolute paths to bluetoothctl and pulseaudio. These should be correct but you can double check them by running  
`which bluetoothctl`  
which should return "/usr/bin/bluetoothctl". If the path is different copy it into the `BTCTL` value. You can repeat this for pulseaudio.

## wiring

Setup the wiring like in the above photo and schema.

Note that the Pi's internal pull down resistor must be enabled. This is enabled in the doorbell.py script with the line:  
`GPIO.setup(pinIn, GPIO.IN, GPIO.PUD_DOWN) # set input terminal with internal pull down resistor`  
An external pull down resistor is not required. The internal pull down resistor will stop a floating state on the input (white) wire and will pull the signal to low when the circuit is open. This stops the doorbell from playing randomly. It is also important that the input (white) wire is connected to the LED's cathode (marked with a +).

Many thanks to Core Electronics for [this article](https://forum.core-electronics.com.au/t/433mhz-remote-control-by-hacking-a-wireless-doorbell-arduino-and-raspberry-pi/7799) which inspired my project. It shows how others have wired the same receiver differently and what the other receiver pins do. Note that you could connect the input GPIO on the Pi to one of the pins on the receiver chip (sig1 or sig2) however their pulses are not consistent enough (see pulses folder for more explanation) and can cause voltage spikes (interference) that somehow ignore the effect of the Pi's internal pull down resistor. Using the LED eliminates both these problems.

When the doorbell is pressed the result is to play 2 sounds:  
 - tune from the doorbell receiver's stock list of tunes followed by 
 - your custom meme through the boom speaker

You can select different tunes by holding the small black button on the transmitter. I suggest the standard 3 knocks "tune" as it is short so to not play over the meme. The 3 knock tune is two tunes after "Santa Claus is Coming to Town". Trust me I've looped through them a lot as the tune resets when the receiver is turned off, but the tune will stay the same when rebooting.

## run

You can turn off VNC to reduce power. This is optional but can be done by:  
logging in through SSH and disable VNC with `sudo raspi-config` > Interface Options > VNC > No > Ok > Finish  
  
If running on boot you can start the service by rebooting with  
`sudo reboot -h now`  
Alternatively if not running on boot you can start by running  
`systemctl --user start doorbell.service`  
Either way wait approximately 10 seconds after service starts running before testing  
  
Test the doorbell by pushing the doorbell transmitter  
  
From here the doorbell should work continuously but if there is an error you can check the logs by:  
- log into SSH terminal and run `cat doorbell/doorbell.log`  
  
To temporarily stop the service, either:  
 - run command `systemctl --user stop doorbell.service`  
 - or turn off the pi `sudo shutdown -h now`  
  
To permanently stop the service, run  
`systemctl --user stop doorbell.service`  
`systemctl --user disable doorbell.service`  

# Issues
- ~~Bluetooth isn't always reliable and may not connect. See warning at start of readme.~~ However even if boom never connects the receiver will always play from its built in speaker so marking as complete
