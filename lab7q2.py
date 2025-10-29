import RPi.GPIO as GPIO
import socket
import json

HOST = ''
PORT = 8080

pins = [17, 27, 22]
GPIO.setmode(GPIO.BCM)
pwms = []
for pin in pins:
  GPIO.setup(pin, GPIO.OUT)
  pwm = GPIO.PWM(pin, 1000)
  pwm.start(0)
  pwms.append(pwm)

brightness = [0, 0, 0]

def webpage():
  html = f""" <!DOCTYPE html>
  <html>
    <head>
      <title> LED Brightness Control: </title>
    </head>
    <body>
      <h2>LED Brightness Control</h2>
      <div class="slider-container">
        <label>LED 1 Brightness: <span id="val1">{brightness[0]}</span>%</label><br>
        <input type="range" min="0" max="100" value="{brightness[0]}" id="led1" onchange="updateLED(0, this.value)">
      </div>
      <div class="slider-container">
        <label>LED 2 Brightness: <span id="val2">{brightness[1]}</span>%</label><br>
        <input type="range" min="0" max="100" value="{brightness[1]}" id="led2" onchange="updateLED(1, this.value)">
      </div>
      <div class="slider-container">
        <label>LED 3 Brightness: <span id="val3">{brightness[2]}</span>%</label><br>
        <input type="range" min="0" max="100" value="{brightness[2]}" id="led3" onchange="updateLED(2, this.value)">
      </div>

      <script>
        async function updateLED(led, value) {{
          document.getElementById('val' + (led+1)).textContent = value;
          fetch("/", {{
            method: "POST",
            headers: {{
              "Content-Type": "application/json"
            }},
            body: JSON.stringify({{"led": led, "brightness": value }})
          }});
        }}
      </script>
    </body>
  </html>
  """
  return html
  
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen(3)
print(f"listening on port {PORT}...")

try:
  while True:
    conn, addr = server.accept()
    print("Connected by:", addr)
    request = conn.recv(2048).decode('utf-8', errors='ignore')
   
    if "POST" in request:
      try:
        body = request.split("\r\n\r\n", 1)[1]
        data = json.loads(body)
        led = int(data["led"])
        value = int(data["brightness"])
        brightness[led]=value
        pwms[led].ChangeDutyCycle(value)
        print(f"Updated LED {led+1}, {value}%")
      except Exception as e:
        print("Error updating LED:", e)

      response = "HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\n\r\nOK"
      conn.sendall(response.encode('utf-8'))

    else:
      response = webpage()
      response_bytes = response.encode('utf-8')
      headers = (
        "HTTP/1.1 200 OK\r\n"
        "Content-Type: text/html\r\n"
        f"Content-Length: {len(response_bytes)}\r\n"
        "Connection: close\r\n\r\n"
      )

      conn.sendall(headers.encode('utf-8') + response_bytes)
    conn.close()

except KeyboardInterrupt:
  for pwm in pwms:
    pwm.stop()
  GPIO.cleanup()
  server.close()

    
