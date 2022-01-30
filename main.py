import time
import machine
from lib import aht20
from lib import pico_i2c_lcd


def print_lcd(display, temp, humidity):
    display.clear()

    display.move_to(0, 0)
    display.putstr(f"Temp:{round(temp, 2)} C")

    display.move_to(0, 1)
    display.putstr(f"Humidity:{round(humidity, 2)} %")


def main():
    onboard_led = machine.Pin(25, machine.Pin.OUT)
    onboard_led.on()

    i2c = machine.I2C(0, scl=machine.Pin(9), sda=machine.Pin(8), freq=100000)

    sensor = aht20.AHT20(i2c)
    display = pico_i2c_lcd.I2cLcd(i2c, 2, 16)

    while True:
        print_lcd(display, sensor.temperature(), sensor.relative_humidity())

        time.sleep(3)


if __name__ == '__main__':
    main()
