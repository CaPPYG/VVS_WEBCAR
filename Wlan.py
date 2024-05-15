import network
import urequests, esp32





class Wifi:
    def __init__(self):
        self.WRITE_API = "6ZJV7YJECK7P1MDQ"
        self.HTTP_HEADER = {'Content-Type': 'application/json'}
        self.wlan = network.WLAN(network.STA_IF)
        self.wlan.active(True)
    def scan_wifi(self):
        networks = self.wlan.scan()
        s = ""
        s += "SSID" + " Security" + "\n"
        s += ("-" * 30) + "\n"
        for ssid, bssid, channel, RSSI, authmode, hidden in networks:
            security = 'open' if authmode == 0 else 'secured'            
            s += ssid.decode('utf-8') + " | " + security + "\n"
        return s
           

    def connect_wifi(self, ssid, password):
        if not self.wlan.isconnected():
            print('Pripajam sa k sieti...')
        self.wlan.connect(ssid, password)
        while not self.wlan.isconnected():
            pass
        return self.wlan.ifconfig()
        
    def run(self):
        self.scan_wifi()
        ssid = input("Zadaj SSID : ")
        password = input("Zadaj heslo: ")
        self.connect_wifi(ssid, password)  # Removed 'self' from the arguments
        while True:
            command = input("Zadaj command (1.measure): ")
            if command.strip() == "measure":
                temperature = {"field1": (esp32.raw_temperature() - 32) * 0.5556}
                request = urequests.post("https://api.thingspeak.com/update?api_key=" + self.WRITE_API, json=temperature,
                                        headers=self.HTTP_HEADER)
                response = request.text
                request.close()
                print("Namerana a odoslana hodnota na Thingspeak: " + str(temperature) + " ID:" + response)
        
    def create_ap():
        ssid = 'ESP32_Garcarz' 
        password = 'garcarz123'  

        ap = network.WLAN(network.AP_IF)
        ap.active(True)
        ap.config(essid=ssid, password=password, authmode=network.AUTH_WPA_WPA2_PSK)

        # Nastavenie statickej IP adresy pre AP
        ap.ifconfig(('192.168.1.1', '255.255.255.0', '192.168.1.1', '8.8.8.8'))

        print('AP running. SSID:', ssid)
        
    


        