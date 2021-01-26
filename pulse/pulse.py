import numpy as np
import os, sys

# buffer for storing bits of one doorbell signal at a time
cap = 200
buffer = np.empty(cap, int)

# stepRange is the number of 0.01s steps between detecting a posible high signal
# chose 40 as lower as there are more above it and 110 as high as most signals are not that long
stepRange = range(40, 110)

def main():
    
    # sort signals into a dictionary and print
    file = open(os.path.join(sys.path[0], 'signals_doorbell.txt'), 'r')
    signalCount = int(file.readline())
    signalDict = {}
    for signalLine in range(signalCount):
        line = file.readline()
        signalDict[line] = []
    
    for signalLine, k in enumerate(signalDict.keys()):
        print(signalLine+1, ': ', k, sep='', end='')
    
    # now print the signal id with steps that produce no errors
    print('\nSignal | steps with no errors')    
    for signalLine, k in enumerate(signalDict.keys()):
        
        # sets buffer and its length
        readBufferLine(k)
        
        for step in stepRange:
            
            isError = False
            for startStep in range(step):
                i = startStep
                while i < length:
                    if buffer[i]:
                        break                  
                    i += step
                    
                if i >= length: # got to end without detecting any highs
                    isError = True
                    break
                
            if not isError:
                # made it to the end of each possible startStep in step without error
                signalDict[k].append(step) # add this step as a no error step for the signal
                
        print(signalLine+1, '     |', signalDict[k])
    
# read line of data into binary int array
def readBufferLine(line):
    global length
    length = 0 # clear the buffer each time
    for char in line:
        if char == '_':
            buffer[length] = 0
            length += 1
        elif char == '-':
            buffer[length] = 1
            length += 1

main()