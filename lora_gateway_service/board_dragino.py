# lora_python_gateway is free software: you can redistribute it and/or
# modify it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# lora_python_gateway is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with lora_python_gateway. If not, see < http://www.gnu.org/licenses/ >.
#
# (C) 2015 by Mayer Analytics Ltd.
# (C) 2017 by Thomas Pointhuber, <thomas.pointhuber@gmx.at>


import RPi.GPIO as GPIO
import spidev

import time


class BOARD_DRAGINO:
    """ Board initialisation/teardown and pin configuration is kept here.
        This is the Raspberry Pi shield by dragino

        based on: https://github.com/mayeranalytics/pySX127x/blob/master/SX127x/board_config.py
    """
    # Note that the BCOM numbering for the GPIOs is used.
    DIO0 = 4    # RaspPi GPIO 4

    # The spi object is kept here
    spi = None

    @staticmethod
    def setup():
        """ Configure the Raspberry GPIOs
        :rtype : None
        """
        GPIO.setmode(GPIO.BCM)
        # DIOx
        GPIO.setup(BOARD_DRAGINO.DIO0, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

    @staticmethod
    def teardown():
        """ Cleanup GPIO and SpiDev """
        GPIO.cleanup()
        BOARD_DRAGINO.spi.close()

    @staticmethod
    def SpiDev(spi_bus=0, spi_cs=0):
        """ Init and return the SpiDev object
        :return: SpiDev object
        :param spi_bus: The RPi SPI bus to use: 0 or 1
        :param spi_cs: The RPi SPI chip select to use: 0 or 1
        :rtype: SpiDev
        """
        BOARD_DRAGINO.spi = spidev.SpiDev()
        BOARD_DRAGINO.spi.open(spi_bus, spi_cs)
        return BOARD_DRAGINO.spi

    @staticmethod
    def add_event_detect(dio_number, callback):
        """ Wraps around the GPIO.add_event_detect function
        :param dio_number: DIO pin 0...5
        :param callback: The function to call when the DIO triggers an IRQ.
        :return: None
        """
        GPIO.add_event_detect(dio_number, GPIO.RISING, callback=callback)

    @staticmethod
    def add_events(cb_dio0, cb_dio1, cb_dio2, cb_dio3, cb_dio4, cb_dio5, switch_cb=None):
        BOARD_DRAGINO.add_event_detect(BOARD_DRAGINO.DIO0, callback=cb_dio0)

    @staticmethod
    def led_on(value=1):
        """ Switch the proto shields LED
        :param value: 0/1 for off/on. Default is 1.
        :return: value
        :rtype : int
        """
        return value

    @staticmethod
    def led_off():
        """ Switch LED off
        :return: 0
        """
        return 0

    @staticmethod
    def blink(time_sec, n_blink):
        pass
