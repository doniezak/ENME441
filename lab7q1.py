import RPI GPIO as GPIO
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
  index = data.find('\r\n\r\n')+4
  data = data[index:]
  pairs = data.split('&')
  for pair in pairs:
    key_value = pair.split('=')
    if len(key_values)==2:
      data_dictionary[key_values[0]]=key_values[1]
  return data_dictionary

def webpage(led1, led2, led3):
  html = f"""
  <html>
    <head><title> Brightness Level: </title></head>
    <body>
      <h2>LED States</h2>
      <p>LED1: {led1}</p>
      <p>LED2:{led2}</p>
      <p>LED 3: {led3}</p>
      
      <form method = "POST">
        <button name="led 1" value="led1"> Click here </button>
        <button name="led 2" value="led2"> Or here </button>
        <button name="led 3" value="led3"> Or here </button>
      </form>
    </body>
  </html>
  """
  return html

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen(3)
print(f"listening on port {PORT}...")
