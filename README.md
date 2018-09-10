# morse-decoder

## Requirements
Python 3  
Keyboard Module  
RPi.GPIO module if you're going to be using this on a Raspberry Pi with GPIO

## What it does
Morse key = q (by default, change the MorseKey variable to the hotkey you will use)   
Dump current set of characters = d (by default, change the DumpKey variable to the hotkey you will use)
Toggle GPIO support = g (by default, change the ToggleGPIO variable to the hotkey you will use)  
If using GPIO, the debounce (time before reading GPIO input) variable can be changed in the code.  
The default pin for GPIO is pin 7, change the GPIOPin variable if you want to use a different pin. The pin will be read as HIGH if there is a 3.3v connected to it and LOW if not. HIGH and LOW are respectively ON and OFF for the morse code key.  
After putting in a set of pulses, wait a bit. There is a timeout when the letter you input is finished. It won't be pushed into the buffer for a few seconds.  
The character set will be printed every 5 seconds by default (*change the DumpInterval variable if you don't want this.*), or you can press the hotkey to dump manually.
Unknown sets of pulses will be replaced with a question mark (?).
