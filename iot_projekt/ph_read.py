import smbus
import time

bus = smbus.SMBus(1) # RPI revision 2 (0 for evision 1)
i2c_address = 0x49 #default address

def Values():
    while True:
         # Reads word (2 bytes) as int - 0 is comm byte
        rd = bus.read_word_data(i2c_address, 0)
        # Echanges high and low bytes
        data = ((rd & 0xFF) << 8) | ((rd & 0xFF00) >> 8)
        # Ignores two least significant bits
        data = data >> 2
        print("Data: ", data)
        #print(data)
        time.sleep(1)
        return data
        
    