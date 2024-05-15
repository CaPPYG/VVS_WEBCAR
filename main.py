from machine import Timer
import Server
import Wlan
import serialRGB
import bluetooth



def main():    
    print("Starting")
    srgb = serialRGB.SerialRGB()
    ble = bluetooth.ESP32_BLE("ESP32_PG")    
    wifi = Wlan.Wifi()
    timer = Timer(0)
    
    
    timer.init(period=500, mode=Timer.PERIODIC, callback=lambda t: srgb.toggle(0))    
    meno = ""
    heslo = ""
    
    while True:       
        if (ble.receivedMessage):
            timer.deinit()
            srgb.set_rgb_color(0, 0, 255, 0)
            ble.send(wifi.scan_wifi() + "\n")
            ble.send("\nZadaj meno\n")
            ble.receivedMessage = None
            while True:
                if (ble.receivedMessage):
                    meno = ble.receivedMessage
                    ble.receivedMessage = None
                    break
            ble.send("\nZadaj heslo\n")
            while True:
                if (ble.receivedMessage):
                    heslo = ble.receivedMessage
                    ble.receivedMessage = None
                    break
            break
      
       
    timer.init(period=500, mode=Timer.PERIODIC, callback=lambda t: srgb.toggle(1))
    
   
    config = wifi.connect_wifi(meno,heslo)
    print("Connected")
    ble.send("Connected")
    
    print(str(config[0]))
    ble.send(str(config[0])) 
      
    timer.deinit()
    srgb.set_rgb_color(1,0,255,0)
    
    timer.init(period=500, mode=Timer.PERIODIC, callback=lambda t: srgb.toggle(2))
    
    print("Starting server...")
    ble.send("Starting server...")
    server = Server.Server()
    server.run(timer, srgb, ble)
    

if __name__ == "__main__":
    main()