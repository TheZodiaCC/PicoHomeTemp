import time
import machine
from lib import aht20
from lib import pico_i2c_lcd
from consts import Consts


class Station:
    def __init__(self):
        self.onboard_led = machine.Pin(25, machine.Pin.OUT)
        self.i2c = machine.I2C(0, scl=machine.Pin(Consts.SCL_PIN), sda=machine.Pin(Consts.SDA_PIN), freq=100000)

        self.temp_sensor = None
        self.display = None

        self.initialized = False

    def init_sensor(self):
        try:
            self.temp_sensor = aht20.AHT20(self.i2c, address=Consts.AHT20_I2C_ADDRESS)
            self.display = pico_i2c_lcd.I2cLcd(self.i2c, Consts.DISPLAY_ROWS, Consts.DISPLAY_CELLS,
                                               i2c_addr=Consts.LCD_DISPLAY_I2C_ADDRESS)

            self.initialized = True

        except Exception as e:
            self.initialized = False

    def print_lcd(self, display, temp, humidity):
        display.clear()

        display.move_to(0, 0)
        display.putstr(f"Temp:     {round(temp, 2)}C")

        display.move_to(0, 1)
        display.putstr(f"Humidity: {round(humidity, 2)}%")

    def process(self):
        while True:
            if self.initialized:
                self.print_lcd(self.display, self.temp_sensor.temperature(), self.temp_sensor.relative_humidity())

            else:
                self.onboard_led.toggle()

            time.sleep(3)

    def run(self):
        self.init_sensor()
        self.process()
