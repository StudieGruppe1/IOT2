# This sample code is used to test the pH meter V1.0.
# Editor : YouYou
# Ver    : 1.0
# Product: analog pH meter
# SKU    : SEN0161

from statistics import mean
from time import time, sleep
import board
import analogio

sensor_pin = analogio.AnalogIn(board.A0)
LED = board.D13
offset = 0.00  # deviation compensate
sampling_interval = 0.02  # 20ms
print_interval = 0.8  # 800ms
array_length = 40  # times of collection
pH_array = [0] * array_length  # Store the average value of the sensor feedback
pH_array_index = 0


def setup():
    global LED
    LED.switch_to_output()
    print("pH meter experiment!")


def loop():
    global pH_array_index
    global pH_array
    sampling_time = time()
    print_time = time()
    while True:
        if time() - sampling_time > sampling_interval:
            pH_array[pH_array_index] = sensor_pin.value
            pH_array_index += 1
            if pH_array_index == array_length:
                pH_array_index = 0
            voltage = mean(pH_array) * 5.0 / 65535
            pH_value = 3.5 * voltage + offset
            sampling_time = time()

        if time() - print_time > print_interval:
            print(f"Voltage: {voltage:.2f}    pH value: {pH_value:.2f}")
            LED.value = not LED.value
            print_time = time()


if __name__ == "__main__":
    setup()
    loop()
