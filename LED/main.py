import RPi.GPIO as GPIO
import time

# Define GPIO pins for the three-position switch
GPIO_COMMON = 27    # Common terminal, set as an output
GPIO_LOAD_A = 22    # Traveler terminal 1, set as an input
GPIO_LOAD_B = 17    # Traveler terminal 2, set as an input
GPIO_LED_RED = 2  # Red LED for neutral position
GPIO_LED_GREEN = 4  # Green LED for Load A
GPIO_LED_BLUE = 3  # Blue LED for Load B

class limitswitch():
    def __init__(self, input_pin, red, green):
        self.input_pin = input_pin
        self.red = red
        self.green = green

        GPIO.BCM
        GPIO.setup(self.input_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self.red, GPIO.OUT)
        GPIO.setup(self.green, GPIO.OUT)

    def update(self):
        state = GPIO.input(self.input_pin)
        if state == GPIO.LOW:  # Assuming LOW means the switch is activated
            GPIO.output(self.red, GPIO.HIGH)
            GPIO.output(self.green, GPIO.LOW)
        else:
            GPIO.output(self.green, GPIO.HIGH)
            GPIO.output(self.red, GPIO.LOW)

class SwitchWithLED:
    def __init__(self, input_pin, led_a, led_b=None):
        self.input_pin = input_pin
        self.led_a = led_a
        self.led_b = led_b

        GPIO.setup(self.input_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self.led_a, GPIO.OUT)
        if self.led_b:
            GPIO.setup(self.led_b, GPIO.OUT)

    def update(self):
        state = GPIO.input(self.input_pin)
        if state == GPIO.LOW:
            GPIO.output(self.led_a, GPIO.HIGH)
            if self.led_b:
                GPIO.output(self.led_b, GPIO.LOW)
        else:
            GPIO.output(self.led_a, GPIO.LOW)
            if self.led_b:
                GPIO.output(self.led_b, GPIO.HIGH)

def setup_gpio():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(GPIO_COMMON, GPIO.OUT)
    GPIO.output(GPIO_COMMON, GPIO.HIGH)
    GPIO.setup(GPIO_LOAD_A, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(GPIO_LOAD_B, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(GPIO_LED_RED, GPIO.OUT)
    GPIO.setup(GPIO_LED_GREEN, GPIO.OUT)
    GPIO.setup(GPIO_LED_BLUE, GPIO.OUT)

def read_switch_update_leds():
    load_a_active = GPIO.input(GPIO_LOAD_A)
    load_b_active = GPIO.input(GPIO_LOAD_B)
    if load_a_active:
        GPIO.output(GPIO_LED_GREEN, GPIO.HIGH)
        GPIO.output(GPIO_LED_BLUE, GPIO.LOW)
        print('load a')
        GPIO.output(GPIO_LED_RED, GPIO.LOW)
    elif load_b_active:
        GPIO.output(GPIO_LED_BLUE, GPIO.HIGH)
        GPIO.output(GPIO_LED_GREEN, GPIO.LOW)
        print('load b')
        GPIO.output(GPIO_LED_RED, GPIO.LOW)
    else:
        GPIO.output(GPIO_LED_RED, GPIO.HIGH)
        GPIO.output(GPIO_LED_GREEN, GPIO.LOW)
        GPIO.output(GPIO_LED_BLUE, GPIO.LOW)

def main():
    GPIO.cleanup()
    setup_gpio()
    switches = [
        SwitchWithLED(16, 20, 21),  # Burn wire switch
        SwitchWithLED(1, 8, 7),  # Linear actuator switch
        SwitchWithLED(0, 6, 5)  # Solenoid switch
    ]
    x = True
    launchConfirm = limitswitch(x, 24, 23)  # Update with the correct GPIO pin for the limit switch
    DampConfirm = limitswitch(x, 15, 14)    # Update with the correct GPIO pin for the limit switch

    try:
        while True:
            read_switch_update_leds()  # Update the three-position switch state
            for switch in switches:
                switch.update()  # Update other switches state
            time.sleep(0.05)

    except KeyboardInterrupt:
        print("Program terminated by user.")
    finally:
        GPIO.cleanup()

if __name__ == "__main__":
    main()

