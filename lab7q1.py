import RPi.GPIO as GPIO
import socket

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

def splitData(data):
  data_dictionary = {}
  index = data.find('\r\n\r\n') + 4
  data = data[index:]
  pairs = data.split('&')
  for pair in pairs:
    key_value = pair.split('=')
    if len(key_value) == 2:
      data_dictionary[key_value[0]]=key_value[1]
  return data_dictionary

def webpage(led1, led2, led3):
  html = f"""
  <html>
    <head>
      <title> Brightness Level: </title>
    </head>
    <body>
      <h2>LED Brightness</h2>
      <p>LED1 Brightness: {led1}%</p>
      <p>LED2 Brightness:{led2}%</p>
      <p>LED3 Brightness: {led3}%</p>
      
      <form method = "POST">
        <label><input type="radio" name="led" value="0" checked> LED 1</label><br>
        <label><input type="radio" name="led" value="1"> LED2</label><br>
        <label><input type="radio" name="led" value="2"> LED3</label><br><br>
        <input type="range" name="brightness" min="0" max="100" value="0"/>
        <input type="submit" value="Set Brightness">
      </form>
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
    request = conn.recv(1024).decode('utf-8')
    print("Request received:\n", request)
   
    if "POST" in request:
      post_dictionary = splitData(request)
      try:
        led = int(post_dictionary.get("led", "0"))
        value = int(post_dictionary.get("brightness", "0"))
        brightness[led]=value
        pwms[led].ChangeDutyCycle(value)
        print(f"Updated LED {led+1}, {value}%brightness")
      except Exception as e:
        print("Error updating LED:", e)
      
    response = webpage(brightness[0], brightness[1], brightness[2])
    response_bytes = response.encode('utf-8')
    conn.send(b"HTTP/1.1 200 OK\r\n")
    conn.send(b"Content-Type: text/html\r\n\r\n")
    conn.send(f"Content-Length: {len(response_bytes)}\r\n\r\n".encode())
    conn.send(b"Connection: close\r\n\r\n")
    conn.sendall(response_bytes)
    conn.close()

except KeyboardInterrupt:
  for pwm in pwms:
    pwm.stop()
  GPIO.cleanup()

    
