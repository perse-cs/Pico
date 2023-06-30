import machine
import time
# Connect Annode of LED to GP5 and cathode to GND
# Use 100-150 ohm resistor

led = machine.Pin(5, machine.Pin.OUT)

while True:
    led.toggle()
    time.sleep(2)