# morse-decoder

## Requirements
Python 3  
Keyboard Module  

## What it does
Morse key = q (by default, change the MorseKey variable to the hotkey you will use)   
Toggle GPIO support = q (by default, change the ToggleGPIO variable to the hotkey you will use)  
The default pin for GPIO is pin 7, change the GPIOPin variable if you want to use a different pin. The pin will be read as HIGH if there is a 3.3v connected to it and LOW if not. HIGH and LOW are respectively ON and OFF for the morse code key.  
After putting in a set of pulses, wait a bit. There is a timeout when the letter you input is finished. It won't be pushed into the buffer for a few seconds.  
Then, the console will be spammed with the list of letters you've typed. Input again at any time.  
Unknown sets of pulses will be replaced with a question mark (?).
