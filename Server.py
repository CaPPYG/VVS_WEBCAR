from machine import Timer
import socket
import serialRGB
import motory



def web_page():   
  
  
  html = """<!DOCTYPE html>
<html>
<head>
  <title>ESP Web Server</title>
  <meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1">
  <link rel="icon" href="data:,">
  <style>
    html {
      font-family: Helvetica, Arial, sans-serif;
      text-align: center;
    }
    h1 {
      color: #0F3376;
      padding: 2vh;
      font-size: 24px;
    }
    p {
      font-size: 18px;
    }
    .button {
      display: inline-block;
      background-color: #e7bd3b;
      border: none;
      border-radius: 4px;
      color: white;
      padding: 12px 24px;
      text-decoration: none;
      font-size: 20px;
      margin: 10px;
      cursor: pointer;
    }
    .button2 {
      background-color: #4286f4;
    }
    .button-row {
      display: flex;
      justify-content: center;
      flex-wrap: wrap;
    }
  </style>
</head>
<body>
  <h1>ESP Web Server</h1>
  <p>Speed Mode:</p>
  <div class="button-row">
    <p><a href="/?speed=slow"><button class="button">Slow</button></a></p>
    <p><a href="/?speed=normal"><button class="button">Normal</button></a></p>
    <p><a href="/?speed=fast"><button class="button">Fast</button></a></p>
  </div>
  <p>Direction:</p>
  <p><a href="/?direction=up"><button class="button">Up</button></a></p>
  <div class="button-row">
    <p><a href="/?direction=left"><button class="button">Left</button></a></p>
    <p><a href="/?direction=stop"><button class="button button2">Stop</button></a></p>
    <p><a href="/?direction=right"><button class="button">Right</button></a></p>
  </div>
  <p><a href="/?direction=down"><button class="button">Down</button></a></p>
</body>
</html>

"""
  return html


class Server:
    def __init__(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.bind(('', 80)) 
        self.timer = Timer(0) 
        self.motors= motory.Motory()
        self.speed = 206     
        

    def run(self, timer, sRgb, ble):        
        while True:
            print('Server running.. ')
            ble.send("Server running")
            
            timer.init(period=500, mode=Timer.PERIODIC, callback=lambda t: sRgb.toggle(2))
            self.s.listen() 
            conn, addr = self.s.accept()
            timer.deinit()
            sRgb.set_rgb_color(2, 0,255,0)
            
            
            print('Got a connection from %s' % str(addr))
            ble.send('Got a connection from %s' % str(addr))
            timer.deinit()
            sRgb.allSet()
            
            
                
            print("receiving")
            request = conn.recv(1024)
            request = str(request)
            print('Content = %s' % request)
            
            up = request.find('/?direction=up')
            down = request.find('/?direction=down')
            left = request.find('/?direction=left')
            right = request.find('/?direction=right')
            stop = request.find('/?direction=stop')
            
            slow = request.find('/?speed=slow')
            normal = request.find('/?speed=normal')
            fast = request.find('/?speed=fast')
            
            if up == 6:
                print('Up')
                self.motors.forward(self.speed)
                
            elif down == 6:
                print('Down')
                self.motors.backward(self.speed)
                
            elif left == 6:
                print('Left')
                self.motors.left(self.speed)
                
            elif right == 6:
                print('Right')
                self.motors.right(self.speed)
            elif stop == 6:
                print('Stop')
                self.motors.stop_motory()
            elif slow == 6:
                print('Slow')
                self.speed = 150
            elif normal == 6:
                print('Normal')
                self.speed = 309
            elif fast == 6:
                print('Fast')
                self.speed = 1023
                
            response = web_page()
            conn.send('HTTP/1.1 200 OK\n')
            conn.send('Content-Type: text/html\n')
            conn.send('Connection: close\n\n')
            conn.sendall(response.encode())
            conn.close()  
                     
                
                      
    

    def stop(self):
        self.s.close()


