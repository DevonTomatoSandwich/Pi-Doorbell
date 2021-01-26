#!/usr/bin/env bash

# These constants must be changed by you
readonly BOOM_HEX="C0:28:8D:F4:4C:01"
readonly BOOM_VALUE="5C5181FEE5AC01"
readonly BOOM_HANDLE="0x0003"
readonly BOOM_CARD="bluez_card.C0_28_8D_F4_4C_01"

# These constants should be checked by you
readonly BTCTL="/usr/bin/bluetoothctl"
readonly PA="/usr/bin/pulseaudio"

function main {
    echo "Running play.sh as $(whoami)"
    paOn 
    speakerOn
    connectBT 2
    play "$1"
}

# Turns pulseaudio on (if not already)
function paOn {
    # initial check for PA
    if [[ ! -z $(pgrep "pulse") ]];
    then
        echo "PA was already on"
        return 0
    else
        echo "PA was off, attempting to start..."
        
        # starts pulse
        echo "Starting pulse..."
        $PA -D --exit-idle-time -1 --verbose
        sleep 1
        # check again for PA
        if [[ ! -z $(pgrep "pulse") ]];
        then
            echo "PA started"
            return 0
        fi
        echo "PA could not be started"
        return 1
    fi
}

# Turns speaker on (if not already)
function speakerOn {
    out="$(gatttool -i hci0 -b "$BOOM_HEX" --char-write-req -a "$BOOM_HANDLE" -n "$BOOM_VALUE")"
    if [ "${out}" == "Characteristic value was written successfully" ]
    then
        echo "Speaker on"
    else
        echo "WARNING: Speaker was not turned on. WARNING: ${out}"
    fi
}

# Connects pi to boom via bluetooth
function connectBT {
    attempts=$1
    while [ $attempts -gt 0 ]
    do
        echo "connecting with $1 attempts left"
        $BTCTL -- connect "$BOOM_HEX"
        $BTCTL -- quit
        
        # ensures the bluez card is sinked 
        pactl set-card-profile "$BOOM_CARD" a2dp_sink && {
            echo "Connected"
            return 0
        }
        
        ((attempts=attempts-1))
    done
    echo "Warning: Device was never connected..."
    return 1
}

# plays sound
function play {
    # plays the sound file (param is a path to .wav from root directory)
    echo "Attempting to play ${1}"
    cd /
    paplay "$1" || echo "Sound not played"
}

main $1