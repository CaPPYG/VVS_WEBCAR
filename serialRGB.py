from machine import Pin, ADC, DAC # type: ignore
import neopixel # type: ignore

class SerialRGB():
    def __init__(self, pin=13, count=3):
        self.np = neopixel.NeoPixel(Pin(13), 3)
        self.led_state = False
        

    def set_rgb_color(self, led, red_intensity, green_intensity, blue_intensity):
        if 0 <= led < len(self.np):
            self.np[led] = (red_intensity, green_intensity, blue_intensity)
            self.np.write()
        else:
            print("Invalid LED index. LED index should be between 0 and", len(self.np) - 1)
            
    def toggle(self, led):        
        if 0 <= led < len(self.np):
            self.led_state = not self.led_state  
            
            
            if self.led_state:
                self.np[led] = (255, 0, 0) 
            else:
                self.np[led] = (0, 0, 0) 
            self.np.write() 
            
    def allSet(self):
        for i in range(len(self.np)):
            self.np[i] = (0, 255, 0)
        self.np.write()
        
