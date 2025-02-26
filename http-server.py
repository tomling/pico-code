import network
import socket
import time
from machine import Pin

# Initialize onboard LED (Pico W uses "LED" pin)
led = Pin("LED", Pin.OUT)

# Replace with your Wi-Fi credentials
SSID = ''
PASSWORD = ''
# Connect to Wi-Fi
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(SSID, PASSWORD)

# Wait for connection
max_wait = 10
while max_wait > 0:
    if wlan.status() < 0 or wlan.status() >= 3:
        break
    max_wait -= 1
    print('Connecting to Wi-Fi...')
    time.sleep(1)

# Check connection status
if wlan.status() != 3:
    led.off()  # Turn off LED if connection failed
    raise RuntimeError('Failed to connect to Wi-Fi')
else:
    ip = wlan.ifconfig()[0]
    print('Connected to Wi-Fi, IP:', ip)
    led.on()  # Turn on LED when connected

# Create a basic web page
def web_page():
    html = """
    <html>
    <head><title>Pico W HTTP Server</title></head>
    <body>
        <h1>Hello from Raspberry Pi Pico W!</h1>
        <p>LED is ON - Server is Running</p>
    </body>
    </html>
    """
    return html

# Set up and start HTTP server
addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
s = socket.socket()
s.bind(addr)
s.listen(1)

print('HTTP server running at http://{}/'.format(ip))

try:
    while True:
        try:
            conn, addr = s.accept()
            print('Connection from', addr)
            
            request = conn.recv(1024)
            print('Request:', request)
            
            response = web_page()
            conn.send('HTTP/1.1 200 OK\n')
            conn.send('Content-Type: text/html\n')
            conn.send('Connection: close\n\n')
            conn.sendall(response)
            conn.close()
        except Exception as e:
            print('Error handling connection:', e)
            conn.close()
except KeyboardInterrupt:
    print("Server stopped by user.")
    led.off()  # Turn off LED when server stops
    s.close()
