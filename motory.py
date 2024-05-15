from machine import Pin, PWM
import time

class Motory():
    def __init__(self):
        self.power_pin = Pin(5, Pin.OUT)
        self.sleep_pin = Pin(22, Pin.OUT)
        self.power_pin.value(1)
        self.sleep_pin.value(1)
        self.in1 = PWM(Pin(15), freq=500)
        self.in2 = PWM(Pin(2), freq=500)
        self.in3 = PWM(Pin(0), freq=500)
        self.in4 = PWM(Pin(4), freq=500)
    def motor1(self,rýchlosť):
        if rýchlosť >= 0:
            self.in1.duty(rýchlosť)
            self.in2.duty(0)
        else:
            self.in1.duty(0) 
            self.in2.duty(-rýchlosť)
    def motor2(self,rýchlosť):
        if rýchlosť >= 0:
            self.in3.duty(rýchlosť)
            self.in4.duty(0)
        else:
            self.in3.duty(0)
            self.in4.duty(-rýchlosť)
    def stop_motory(self):
            self.in1.duty(0)
            self.in2.duty(0)
            self.in3.duty(0)
            self.in4.duty(0)
    
    def forward(self, speed):
        # Move forward
        self.motor1(speed)
        self.motor2(speed)
        
    def backward(self, speed):
        # Move backward
        self.motor1(-speed)  # Negative speed for reverse direction
        self.motor2(-speed)  # Negative speed for reverse direction
        
    def left(self, speed):
        # Turn left
        self.motor1(speed)  # Negative speed for reverse direction
        self.motor2(-speed)
        
    def right(self, speed):
        # Turn right
        self.motor1(-speed)
        self.motor2(speed)  # Negative speed for reverse direction
    
#motory = Motory()
#rýchlosť_motor1 = 1023
#rýchlosť_motor2 = 1023
#motory.motor1(rýchlosť_motor1)
#motory.motor2(rýchlosť_motor2)
#time.sleep(5)
#motory.stop_motory()
