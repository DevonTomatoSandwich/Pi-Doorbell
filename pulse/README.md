# Pulse

The purpose of this folder is to show calcultion for the checking interval (0.46s) used in doorbell.py to listen for high input. 

Where any signal is displayed, either below or in the files, a low reading is "_" and a high reading is "-" each reading represents a timestep of 0.01s. 

## Using reciever pins

A typical signal from the reciever pins (sig1 or sig2) is:  
-_-__--_____-_____-_-___-_-____--_-__--_-___-__-____________________________________________________________________________________________________--_-__--_-__--_-__----  
 but this signal is not consistent and will not always have two main peaks for example  
-_____-_-_____-_-__--_-___-__-__-__-_--_-_--__---  

another thing to note is that the highs in the first peak don't match up and arn't ever in consistent places. See pulse.txt for more examples

another problem is the susceptibility of these pins from interference. A phantom signal is mostly like this  
\-  
however i have recorded some like this  
-_________-  
it can be slightly difficult to tell a phantom signal apart from a actual doorbell signal 
especially if you are trying to improve efficiency by limiting the number of checks per second  

## Using LED cathode +

A typical signal from the LED is:  

----------------\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_----------------\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_----------------\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_----------------  

this has very slight variation. See pulse.txt for more examples  

a benefit of the LED is that there is no interference (that I've observed so far) even when taking readings every 0.01s.  

So all you have to do is find one high in the above signal and its slight variations  

## The scripts

Clearly the LED is chosen as the input over the pins.  
  
Now efficiency can be improved by maximising the checking interval.
pulse.py runs through all 28 raw inputs and its output is in pulse.txt
The results are that there are 4 unique signals all very similar, and that using a timestep of 48 or checking interval of 0.48s,
you will never miss any of the highs in the signal.  
  
Allowing for unaccounted-for variations that may not be included in the 28 samples, I decided on a checking interval of 0.46s
