import keyboard
import time

OffThreshold = 900 #Threshold until characters are sent to TotalBuffer
ShortThreshold = 90 #The max amount of cycles until a pulse is determined to be LONG.
MessageTime = 0.0 #The amount of time a non-full-debug message will stay on screen. Set to 0 to disable debug.
LongMessageTime = 0.5 #The amount of time a long debug message should stay. Set to 0 to disable debug.

SingleBuffer = "" #Pulses written before cleared.
TotalBuffer = [] #Set of letters.
FinishedBuffer = [] #Set of letters converted from Morse.

Morse = ['.-', '-...', '-.-.', '-..', '.', '..-.', '--.', '....', '..', '.---', '-.-', '.-..', '--', '-.', '---', '.--.', '--.-', '.-.', '...', '-', '..-', '...-', '.--', '-..-', '-.--', '--..']
Alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']

if not (len(Morse) == len(Alphabet)):
    print("Morse length != Alphabet length!!!")

def dbg(toLog):
    #print(toLog)
    KeyPressing() #python requires a thing to be used

def impdbg(toLog):
    #print(toLog)
    KeyPressing()

def simpdbg(toLog):
    print(toLog)

def KeyPressing():
    return keyboard.is_pressed('q')

def DebugBuffer():
    if keyboard.is_pressed('y'):
        impdbg(TotalBuffer)
        for pulses in TotalBuffer:
            impdbg(pulses)
            try:
                impdbg(Morse.index(pulses))
                impdbg(Alphabet[Morse.index(pulses)])
                FinishedBuffer.append(Alphabet[Morse.index(pulses)])
            except:
                FinishedBuffer.append("?")
        simpdbg(FinishedBuffer)
        time.sleep(LongMessageTime)
                
            
    

while True: #needed to break, but breaking is broken :(
    
    while True:
        OnTime = 0.0
        OffTime = 0.0
        
        while (not (KeyPressing())):
            DebugBuffer()
            dbg("Key off")
            OffTime += 0.1
            dbg(OffTime)
            if (OffTime >= OffThreshold):
                simpdbg("END")
                impdbg(SingleBuffer)
                if not (SingleBuffer == ""):
                    TotalBuffer.append(SingleBuffer)
                SingleBuffer = ""
                time.sleep(MessageTime)
                OffTime = 0
                OnTime = 0
            

        impdbg("Key on")
        while (KeyPressing()):
            OnTime += 0.1
            dbg(OnTime)

        if (OnTime <= ShortThreshold):
            SingleBuffer = SingleBuffer + "."
            simpdbg("SHORT")
        else:
            SingleBuffer = SingleBuffer + "-"
            simpdbg("LONG")
        OffTime = 0.0 #Reset the time-till-timeout to give user enough input time.

        time.sleep(MessageTime)
        
