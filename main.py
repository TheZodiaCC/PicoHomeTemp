import utime
import machine
import aht20


def main():
    onboard_led = machine.Pin(25, machine.Pin.OUT)
    onboard_led.on()

    i2c = machine.I2C(0, scl=machine.Pin(9), sda=machine.Pin(8), freq=400000)
    # print(hex(i2c.scan()[0]))

    sensor = aht20.AHT20(i2c)

    while True:
        print(f"Temperature: {sensor.temperature()} C")
        print(f"Humidity: {sensor.relative_humidity()}")

        utime.sleep(1)


if __name__ == '__main__':
    main()
