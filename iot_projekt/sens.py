import neopixel
import board
import sqlite3
import smbus
import time

bus = smbus.SMBus(1) # RPI revision 2 (0 for evision 1)
i2c_address = 0x49 #default address

# Initialize NeoPixel LED ring
pixel_pin = board.D10
num_pixels = 12
ORDER = neopixel.GRB
pixels = neopixel.NeoPixel(pixel_pin, num_pixels, brightness=0.2, auto_write=True, pixel_order=ORDER)


def read_ph_sensor():
    #while True:
        # Reads word (2 bytes) as int - 0 is comm byte
    rd = bus.read_word_data(i2c_address, 0)
        # Echanges high and low bytes
    ANALOG_VALUE = ((rd & 0xFF) << 8) | ((rd & 0xFF00) >> 8)
        # Ignores two least significant bits
    ANALOG_VALUE = ANALOG_VALUE >> 2
    print("Data: ", ANALOG_VALUE)
        #print(data)
    return ANALOG_VALUE
    time.sleep(1)

def set_neopixel_leds(ANALOG_VALUE):
    while True:
    # code to set NeoPixel LED color based on pH value through the ranges listed above
        try:
            if ANALOG_VALUE <= 15:
                pixels.fill((255, 0, 0))
                print("PH value is '0")
                PH_VALUE = 0
            elif ANALOG_VALUE <= 30:
                pixels.fill((255, 94, 0))
                print("PH value is '1")
                PH_VALUE = 1
            elif ANALOG_VALUE <= 50:
                pixels.fill((255, 179, 0))
                print("PH value is '2")
                PH_VALUE = 2
            elif ANALOG_VALUE <= 80:
                pixels.fill((255, 255, 0))
                print("PH value is '3")
                PH_VALUE = 3
            elif ANALOG_VALUE <= 160:
                pixels.fill((191, 255, 0))
                print("PH value is '4")
                PH_VALUE = 4
            elif ANALOG_VALUE <= 300:
                pixels.fill((128, 255, 0))
                print("PH value is '5")
                PH_VALUE = 5
            elif ANALOG_VALUE <= 450:
                pixels.fill((64, 255, 0))
                print("PH value is '6")
                PH_VALUE = 6
            elif ANALOG_VALUE <= 600:
                pixels.fill((0, 255, 0))
                print("PH value is '7")
                PH_VALUE = 7
            elif ANALOG_VALUE <= 650:
                pixels.fill((0, 255, 64))
                print("PH value is '8")
                PH_VALUE = 8
            elif ANALOG_VALUE<= 700:
                pixels.fill((0, 255, 128))
                print("PH value is '9")
                PH_VALUE = 9
            elif ANALOG_VALUE<= 750:
                pixels.fill((0, 255, 191))
                print("PH value is '10")
                PH_VALUE = 10
            elif ANALOG_VALUE <= 800:
                pixels.fill((0, 255, 255))
                print("PH value is '11")
                PH_VALUE = 11
            elif ANALOG_VALUE<= 900:
                pixels.fill((0, 128, 255))
                print("PH value is '12")
                PH_VALUE = 12
            elif ANALOG_VALUE <= 1000:
                pixels.fill((0, 0, 255))
                print("PH value is '13")
                PH_VALUE = 13
            return PH_VALUE
            time.sleep(1)
        except KeyboardInterrupt:
            pixels.fill((0,0,0))
            pixels.show()

#Main program loop
#try:
#    while True:
#        ANALOG_VALUE = read_ph_sensor()  # read pH sensor
#        set_neopixel_leds(ANALOG_VALUE)  # set NeoPixel LED color based on pH value
#except KeyboardInterrupt:
#    pixels.fill((0,0,0))
#    pixels.show()