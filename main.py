import keyboard
import time

MorseKey = 'q'

OffThreshold = 900 #Threshold until characters are sent to TotalBuffer
ShortThreshold = 100 #The max amount of cycles until a pulse is determined to be LONG.
MessageTime = 0.0 #The amount of time a non-full-debug message will stay on screen. Set to 0 to disable debug.
LongMessageTime = 0.5 #The amount of time a long debug message should stay. Set to 0 to disable debug.

SingleBuffer = "" #Pulses written before cleared.
TotalBuffer = [] #Set of letters.
FinishedBuffer = [] #Set of letters converted from Morse.

Morse = ['.-', '-...', '-.-.', '-..', '.', '..-.', '--.', '....', '..', '.---', '-.-', '.-..', '--', '-.', '---', '.--.', '--.-', '.-.', '...', '-', '..-', '...-', '.--', '-..-', '-.--', '--..', '.----', '..---', '...--', '....-', '.....', '-....', '--...', '---..', '----.', '-----']
Alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0']


OnTime = 0.0 #Current pulse time
OffTime = 0.0 #Idle time

        
if not (len(Morse) == len(Alphabet)):
    print("Morse length != Alphabet length!!!")

def resetvars():
    OnTime = 0.0
    OffTime = 0.0
    SingleBuffer = ""
    FinishedBuffer = []
    FinishedBuffer.clear()

def dbg(toLog):
    #print(toLog)
    KeyPressing() #python requires a thing to be used

def impdbg(toLog):
    #print(toLog)
    KeyPressing()

def simpdbg(toLog):
    print(toLog)

def KeyPressing():
    return keyboard.is_pressed(MorseKey)

def DebugBuffer():
    FinishedBuffer.clear()
    #simpdbg(TotalBuffer)
    for pulses in TotalBuffer:
     #impdbg(pulses)
     try:
         #impdbg(Morse.index(pulses))
         #impdbg(Alphabet[Morse.index(pulses)])
         FinishedBuffer.append(Alphabet[Morse.index(pulses)])
     except:
        FinishedBuffer.append("?")
         
    simpdbg("".join(FinishedBuffer))
    resetvars()
                
            
    

while True:
    
    while True:
        
        resetvars()
        
        while (not (KeyPressing())):
            dbg("Key off")
            OffTime += 0.1
            dbg(OffTime)
            if (OffTime >= OffThreshold):
                impdbg("END")
                impdbg(SingleBuffer)
                if not (SingleBuffer == ""):
                    TotalBuffer.append(SingleBuffer)
                SingleBuffer = ""
                DebugBuffer()
                time.sleep(MessageTime)
                resetvars()
            

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
        OnTime = 0.0
        OffTime = 0.0 #Reset the time-till-timeout to give user enough input time.

        time.sleep(MessageTime)
        
