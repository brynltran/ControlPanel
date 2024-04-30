#!/home/controlpanel/controlpanel/.control-panel-venv/bin/python
import RPi.GPIO as GPIO
import time
import socket
# Define GPIO pins for the three-position switch
GPIO_COMMON = 27    # Common terminal, set as an output
GPIO_LOAD_A = 22    # Traveler terminal 1, set as an input
GPIO_LOAD_B = 17    # Traveler terminal 2, set as an input
GPIO_LED_RED = 2  # Red LED for neutral position
GPIO_LED_GREEN = 4  # Green LED for Load A
GPIO_LED_BLUE = 3  # Blue LED for Load B

def start_server():

    switches = [
        SwitchWithLED(16, 20, 21),  # Burn wire switch
        SwitchWithLED(1, 8, 7),  # Linear actuator switch
        SwitchWithLED(0, 6, 5)  # Solenoid switch
    ]
    host = '192.168.1.2'  # Localhost
    port = 1313        # Choose any port that is free on your system
    
    # Create a socket object
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1) 
    # Bind the socket to the host and port
    server_socket.bind((host, port))
    # Listen for incoming connections
    server_socket.listen()
    print("Server is listening on", host, port)
    
    while True:
        # Accept a connection

        for switch in switches:
            switch.off()
            print(switch)
        restOff()
        TCPWait()
        client_socket, addr = server_socket.accept()
        print('Connected by', addr)
        launchConfirm = limitswitch(False, 9, 11)  #Initialize Limit Switch lights to red 
        DampConfirm = limitswitch(False, 14, 15)     
        
        try:
            while True:
                print("Here")
                # Receive data from the client
                data = client_socket.recv(1024)
                read_switch_update_leds()  # Update the three-position switch state

                for switch in switches:
                    switch.update()  # Update other switches state
                # Optionally, send some data back
                client_socket.sendall(b'Echo => ' + data)
        except socket.error as e:
            print("Socket error:", e)
        finally:
            client_socket.close()

        print('Connection closed with', addr)
def TCPWait():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(20, GPIO.OUT)
    GPIO.setup(21, GPIO.OUT)
    GPIO.setup(8, GPIO.OUT)
    GPIO.setup(7, GPIO.OUT)
    GPIO.setup(6, GPIO.OUT)
    GPIO.setup(5, GPIO.OUT)
    GPIO.setup(9, GPIO.OUT)
    GPIO.setup(11, GPIO.OUT)
    GPIO.setup(14, GPIO.OUT)
    GPIO.setup(15, GPIO.OUT)
    GPIO.setup(2, GPIO.OUT)
    GPIO.setup(4, GPIO.OUT)
    GPIO.setup(3, GPIO.OUT)


    GPIO.output(20, GPIO.LOW)
    GPIO.output(21, GPIO.LOW)
    GPIO.output(8, GPIO.LOW)
    GPIO.output(7, GPIO.LOW)
    GPIO.output(6, GPIO.LOW)
    GPIO.output(5, GPIO.LOW)
    GPIO.output(9, GPIO.LOW)
    GPIO.output(11, GPIO.LOW)
    GPIO.output(14, GPIO.LOW)
    GPIO.output(15, GPIO.LOW)
    GPIO.output(2, GPIO.LOW)
    GPIO.output(4, GPIO.LOW)
    GPIO.output(3, GPIO.LOW)
#blink
    
    GPIO.output(20, GPIO.HIGH)
    time.sleep(0.2)
    GPIO.output(20, GPIO.LOW)
    
    GPIO.output(21, GPIO.HIGH)
    time.sleep(0.2)
    GPIO.output(21, GPIO.LOW)

    GPIO.output(8, GPIO.HIGH)
    time.sleep(0.2)
    GPIO.output(8, GPIO.LOW)

    GPIO.output(7, GPIO.HIGH)
    time.sleep(0.2)
    GPIO.output(7, GPIO.LOW)

    GPIO.output(9, GPIO.HIGH)
    time.sleep(0.2)
    GPIO.output(9, GPIO.LOW)

    GPIO.output(11, GPIO.HIGH)
    time.sleep(0.2)
    GPIO.output(11, GPIO.LOW)

    GPIO.output(6, GPIO.HIGH)
    time.sleep(0.2)
    GPIO.output(6, GPIO.LOW)

    GPIO.output(5, GPIO.HIGH)
    time.sleep(0.2)
    GPIO.output(5, GPIO.LOW)
    

    GPIO.output(14, GPIO.HIGH)
    time.sleep(0.2)
    GPIO.output(14, GPIO.LOW)

    GPIO.output(15, GPIO.HIGH)
    time.sleep(0.2)
    GPIO.output(15, GPIO.LOW)

    GPIO.output(2, GPIO.HIGH)
    time.sleep(0.2)
    GPIO.output(2, GPIO.LOW)

    GPIO.output(4, GPIO.HIGH)
    time.sleep(0.2)
    GPIO.output(4, GPIO.LOW)

    GPIO.output(3, GPIO.HIGH)
    time.sleep(0.2)
    GPIO.output(3, GPIO.LOW)



def restOff():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(9, GPIO.OUT)
    GPIO.setup(11, GPIO.OUT)
    GPIO.setup(14, GPIO.OUT)
    GPIO.setup(15, GPIO.OUT)

    GPIO.output(9, GPIO.LOW)
    GPIO.output(11, GPIO.LOW)
    GPIO.output(14, GPIO.LOW)
    GPIO.output(15, GPIO.LOW)

class limitswitch():
    def __init__(self, initial_state, red, green):
        self.state = initial_state
        self.red = red
        self.green = green

        # Setup the GPIO pins for the LEDs
        GPIO.setup(self.red, GPIO.OUT)
        GPIO.setup(self.green, GPIO.OUT)
        self.update()  # Update the LEDs based on the initial state

    def set_state(self, state):
        self.state = state
        self.update()

    def update(self):
        if self.state:
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
    def off(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.led_a, GPIO.OUT)
        GPIO.setup(self.led_b, GPIO.OUT)
        GPIO.output(self.led_a, GPIO.LOW)
        GPIO.output(self.led_b, GPIO.LOW)
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
        GPIO.output(GPIO_LED_RED, GPIO.LOW)
    elif load_b_active:
        GPIO.output(GPIO_LED_BLUE, GPIO.HIGH)
        GPIO.output(GPIO_LED_GREEN, GPIO.LOW)
        GPIO.output(GPIO_LED_RED, GPIO.LOW)
    else:
        GPIO.output(GPIO_LED_RED, GPIO.HIGH)
        GPIO.output(GPIO_LED_GREEN, GPIO.LOW)
        GPIO.output(GPIO_LED_BLUE, GPIO.LOW)

def main():
    setup_gpio()
    switches = [
        SwitchWithLED(16, 20, 21),  # Burn wire switch
        SwitchWithLED(1, 8, 7),  # Linear actuator switch
        SwitchWithLED(0, 6, 5)  # Solenoid switch
    ]
    launchConfirm = limitswitch(False, 9, 11)  #Initialize Limit Switch lights to red 
    DampConfirm = limitswitch(False, 14, 15)     
    try:
        start_server()
    except KeyboardInterrupt:
        print("program terminated")
    finally:
        GPIO.cleanup()
'''
    try:
        while True:
            read_switch_update_leds()  # Update the three-position switch state
            for switch in switches:
                switch.update()  # Update other switches state
            time.sleep(0.05)
            start_server()
    except KeyboardInterrupt:
        print("Program terminated by user.")
    finally:
        GPIO.cleanup()
'''
if __name__ == "__main__":
    main()

