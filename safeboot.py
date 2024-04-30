import os
import threading
import RPi.GPIO as GPIO
import time
import subprocess
from multiprocessing import Process


GPIO.setmode(GPIO.BCM)
path = '/home/controlpanel/controlpanel/main.py'
python_path = '/home/controlpanel/controlpanel/.control-panel-venv/bin/python'
#led_pins = [2, 3, 9, 11, 5, 6, 14, 15, 8, 7, 16, 20]
led_pins = [20, 21, 8, 7, 6, 5, 9, 11, 14, 15, 2 , 4, 3]
#led_pins = [21, 7, 5, 11, 15]
for pin in led_pins:
    GPIO.setup(pin, GPIO.OUT)  # Set each pin as an output
    GPIO.output(pin, GPIO.LOW)
GPIO.setwarnings(False)
GPIO_COMMON = 27    # Common terminal, set as an output
GPIO_LOAD_A = 22    # Traveler terminal 1, set as an input
GPIO_LOAD_B = 17    # Traveler terminal 2, set as an input
GPIO_LED_RED = 2    # Red LED for neutral position
GPIO_LED_GREEN = 4  # Green LED for Load A
GPIO_LED_BLUE = 3   # Blue LED for Load B

def check_specific_switches():
    """
    Setup, check, and clean up specific GPIO pins for switch status.

    Returns:
        bool: True if any specified switch is active (detected as GPIO.LOW), False otherwise.
    """
    # Define the GPIO pins for the specific switches
    switch_pins = [16, 1, 0]
    
    # Initialize GPIO
    GPIO.setmode(GPIO.BCM)    
    # Setup each switch pin with pull-up resistor
    for pin in switch_pins:
        GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    
    # Check the state of each switch
    any_active = False
    GPIO.setup(GPIO_COMMON, GPIO.OUT)
    GPIO.output(GPIO_COMMON, GPIO.HIGH)  # Normally set to high for the common terminal
    GPIO.setup(GPIO_LOAD_A, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(GPIO_LOAD_B, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    loada = GPIO.input(GPIO_LOAD_A)
    loadb = GPIO.input(GPIO_LOAD_B)
    if loadb:
        print('load b')
        any_active = True
    if loada:
        print('load a')
        any_active = True
    if GPIO.input(switch_pins[0]) == GPIO.HIGH:
        any_active = True
        print(switch_pins[0])
    if GPIO.input(switch_pins[1]) == GPIO.LOW:
        print(switch_pins[1])
        any_active = True
    if GPIO.input(switch_pins[2]) == GPIO.LOW:
        print(switch_pins[2])
        any_active = True
    # Clean up GPIO to ensure there are no conflicts or residual configurations
    return any_active
def setup_and_turn_off_pins():
    """
    Sets up GPIO pins and turns them all off.
    """
    # Set up GPIO mode
    GPIO.setwarnings(False)
    #led_pins = [20, 21, 8, 7, 6, 5, 9, 11, 14, 15, 2 , 4, 3]
    # Setup each pin as an output and set it to low
    for pin in led_pins:
        GPIO.setup(pin, GPIO.OUT)
        GPIO.output(pin, GPIO.LOW)
def setup_leds():
    """Set up GPIO mode and pin output settings for all LEDs."""
    GPIO.setmode(GPIO.BCM)  # Set GPIO numbering based on Broadcom SOC channel numbers
    for pin in led_pins:
        GPIO.setup(pin, GPIO.OUT)  # Set each pin as an output
        GPIO.output(pin, GPIO.LOW)
        


setup_leds()

try:
    for pin in led_pins:
        GPIO.output(pin, GPIO.LOW)
    red = [11, 15]
    while check_specific_switches():
        for pin in red:
            GPIO.output(pin, GPIO.LOW)  # Turn LED on

        time.sleep(0.5)  # Wait for one second
    
        for pin in red:
            GPIO.output(pin, GPIO.HIGH)  # Turn LED on

        time.sleep(0.5)
finally:
    GPIO.cleanup()
subprocess.run(['python', '/home/controlpanel/controlpanel/main.py'])
#GPIO.cleanup()
