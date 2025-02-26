from machine import Pin, SPI
import max7219
from time import sleep

# SPI1 setup (using GP10 for CLK and GP11 for MOSI)
spi = SPI(1, baudrate=10000000, polarity=0, phase=0, sck=Pin(10), mosi=Pin(11))
cs = Pin(13, Pin.OUT)

# Initialize the MAX7219 8x8 matrix
matrix = max7219.Matrix8x8(spi, cs, 1)  # '1' indicates one matrix module
matrix.brightness(5)  # Brightness level (0 to 15)

# Function to display letters A-Z
def flash_alphabet():
    for letter in range(ord('A'), ord('Z') + 1):
        matrix.fill(0)  # Clear display
        matrix.text(chr(letter), 0, 0, 1)  # Display current letter
        matrix.show()
        sleep(0.5)  # Display each letter for 0.5 seconds

    # Clear display after flashing the alphabet
    matrix.fill(0)
    matrix.show()

# Run the alphabet flasher in a loop
try:
    while True:
        flash_alphabet()
        sleep(1)  # Pause before restarting the alphabet
except KeyboardInterrupt:
    # Clean exit on Ctrl+C
    matrix.fill(0)
    matrix.show()
    print("Program stopped.")

