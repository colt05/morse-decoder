import keyboard
import time
import threading

MorseKey = 'q'
ToggleGPIO = 'g'
DumpKey = 'd'
GPIOPin = 7
Debounce = 0.01 #Time in SECONDS before reading GPIO input. Change according to your morse speed (only if using gpio)


canusegpio = True

try:
    import RPi.GPIO as GPIO
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(GPIOPin, GPIO.IN, GPIO.PUD_DOWN) #https://opensourceforu.com/2017/07/introduction-raspberry-pi-gpio-programming-using-python/
except:
    print("Error importing GPIO. It can't be used.")
    canusegpio = False

global UsingGPIO
UsingGPIO = False


OffThreshold = 900 #Threshold until characters are sent to TotalBuffer
ShortThreshold = 100 #The max amount of cycles until a pulse is determined to be LONG.
ShortThresholdGPIO = 3.9 #See the readme
MessageTime = 0.0 #The amount of time a non-full-debug message will stay on screen. Set to 0 to disable debug.
LongMessageTime = 0.5 #The amount of time a long debug message should stay. Set to 0 to disable debug.
DumpInterval = 5.0 #The interval in seconds in which the character set will be dumped.

SingleBuffer = "" #Pulses written before cleared.
TotalBuffer = [] #Set of letters.
FinishedBuffer = [] #Set of letters converted from Morse.

Morse = ['.-', '-...', '-.-.', '-..', '.', '..-.', '--.', '....', '..', '.---', '-.-', '.-..', '--', '-.', '---', '.--.', '--.-', '.-.', '...', '-', '..-', '...-', '.--', '-..-', '-.--', '--..', '.----', '..---', '...--', '....-', '.....', '-....', '--...', '---..', '----.', '-----']
Alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0']


OnTime = 0.0 #Current pulse time
OffTime = 0.0 #Idle time

        
if not (len(Morse) == len(Alphabet)):
    print("Morse length != Alphabet length!!!")

def DoNothing():
    return

def resetvars():
    OnTime = 0.0
    OffTime = 0.0
    SingleBuffer = ""
    FinishedBuffer = []
    FinishedBuffer.clear()

def dbg(toLog):
    #print(toLog)
    DoNothing()

def impdbg(toLog):
    #print(toLog)
    DoNothing()

def simpdbg(toLog):
    print(toLog)

def KeyPressing():
    global UsingGPIO
    try:
        if UsingGPIO:
            time.sleep(Debounce)
            return bool(GPIO.input(GPIOPin))
    except:
        print("Using GPIO failed")
        
    return keyboard.is_pressed(MorseKey)

def CheckToggleGPIO():
    global UsingGPIO # https://stackoverflow.com/questions/18002794/local-variable-referenced-before-assignment-in-python
    if canusegpio:
        if keyboard.is_pressed(ToggleGPIO):
            UsingGPIO = not UsingGPIO
            print(UsingGPIO)
            if UsingGPIO:
                print("Using GPIO!")
                time.sleep(LongMessageTime)
            else:
                print("NOT using GPIO!")
                time.sleep(LongMessageTime)
    else:
        #print("Can't use GPIO!")
        #time.sleep(LongMessageTime)
        DoNothing()

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
                
            
def PeriodicDump(): # https://stackoverflow.com/questions/3393612/run-certain-code-every-n-seconds
    threading.Timer(DumpInterval, PeriodicDump).start()
    DebugBuffer()

def ManualDump():
    if keyboard.is_pressed(DumpKey):
        DebugBuffer()

try:
    PeriodicDump()
    while True:
        
        resetvars()
        CheckToggleGPIO()
        while (not (KeyPressing())):
            dbg("Key off")
            CheckToggleGPIO()
            OffTime += 0.1
            dbg(OffTime)
            if (OffTime >= OffThreshold):
                impdbg("END")
                impdbg(SingleBuffer)
                if not (SingleBuffer == ""):
                    TotalBuffer.append(SingleBuffer)
                SingleBuffer = ""
                time.sleep(MessageTime)
                resetvars()
            

        impdbg("Key on")
        while (KeyPressing()):
            OnTime += 0.1
            dbg(OnTime)

        curThreshold = ShortThreshold
        if UsingGPIO:
            curThreshold = ShortThresholdGPIO
        if (OnTime <= curThreshold):
            SingleBuffer = SingleBuffer + "."
            simpdbg("SHORT")
        else:
            SingleBuffer = SingleBuffer + "-"
            simpdbg("LONG")
        OnTime = 0.0
        OffTime = 0.0 #Reset the time-till-timeout to give user enough input time.
        CheckToggleGPIO()
        time.sleep(MessageTime)

except:
    try:
        GPIO.cleanup()
        print("GPIO cleaned up")
    except:
        print("GPIO not cleaned up")
    
    DebugBuffer()
