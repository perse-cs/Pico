import machine
import time
from picographics import PicoGraphics, DISPLAY_PICO_EXPLORER
from motor import Motor

display = PicoGraphics(display=DISPLAY_PICO_EXPLORER)
WHITE = display.create_pen(255, 255, 255)
BG = display.create_pen(32, 32, 64)
display.set_pen(WHITE)

MOTOR1 = Motor((8, 9))
MOTOR2 = Motor((10, 11))


# Define GPIO pins for trigger and echo
TRIGGER_PIN = 4

ECHO_PIN = 5

# Create objects for trigger and echo pins
trigger = machine.Pin(TRIGGER_PIN, machine.Pin.OUT)
echo = machine.Pin(ECHO_PIN, machine.Pin.IN)

def measure_distance():
    # Generate a 10us pulse on the trigger pin
    trigger.value(0)
    time.sleep_us(2)
    trigger.value(1)
    time.sleep_us(10)
    trigger.value(0)
    
    # Wait for the echo pin to go high
    while echo.value() == 0:
        pass
    pulse_start = time.ticks_us()
    
    # Wait for the echo pin to go low
    while echo.value() == 1:
        pass
    pulse_end = time.ticks_us()
    
    # Calculate the pulse duration and convert it to distance in centimeters
    pulse_duration = pulse_end - pulse_start
    distance_cm = pulse_duration / 58.0
    
    return distance_cm

while True:
    distance = measure_distance()
    output = "Distance: {:.2f} cm".format(distance)
    print(output)
    
    display.set_pen(BG)
    display.clear()
    
    display.set_pen(WHITE)
    display.text(output, 20, 20, 200)
    
    if distance > 10:
        display.text("Motor 1: Forwards", 20, 180, 200)
        MOTOR1.full_positive()
        display.text("Motor 2: Forwards", 20, 200, 200)
        MOTOR2.full_positive()
    else:
        display.text("Motor 1: Backwards", 20, 180, 200)
        MOTOR1.full_negative()
        display.text("Motor 2: Backwards", 20, 200, 200)
        MOTOR2.full_negative()
    
    
    time.sleep(0.1)
    display.update()

