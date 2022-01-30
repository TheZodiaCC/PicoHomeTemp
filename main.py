import time
import machine
from lib import aht20
from lib import pico_i2c_lcd


def scan_i2c_devices(i2c):
    devices = i2c.scan()

    for device in devices:
        print(f"{device} | address {hex(device)}")


def print_lcd(display, temp, humidity):
    display.clear()

    display.move_to(1, 0)
    current_time = time.gmtime()
    display.putstr(f"{current_time[3]}:{current_time[4]}:{current_time[5]}")

    display.move_to(1, 1)
    display.putstr(f"T:{round(temp, 1)}C  ")
    display.putstr(f"H:{int(humidity)}%")


def main():
    onboard_led = machine.Pin(25, machine.Pin.OUT)
    onboard_led.on()

    i2c = machine.I2C(0, scl=machine.Pin(9), sda=machine.Pin(8), freq=100000)

    scan_i2c_devices(i2c)

    sensor = aht20.AHT20(i2c)
    display = pico_i2c_lcd.I2cLcd(i2c, 2, 16)

    while True:
        print_lcd(display, sensor.temperature(), sensor.relative_humidity())

        time.sleep(1)


if __name__ == '__main__':
    main()
