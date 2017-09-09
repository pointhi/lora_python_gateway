#!/usr/bin/env python

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

import signal
import sys, os

from time import sleep

sys.path.append(os.path.join(sys.path[0], "pySX127x")) # load pySX127x path

from SX127x.LoRa import *
from SX127x.LoRaArgumentParser import LoRaArgumentParser

from board_dragino import BOARD_DRAGINO as BOARD

class LoRaGatewayService(LoRa):
    def __init__(self, **kwargs):
        super(LoRaGatewayService, self).__init__(**kwargs)
        self.set_mode(MODE.SLEEP)
        self.set_dio_mapping([0] * 6)

    def on_rx_done(self):
        BOARD.led_on()
        print("\nRxDone")
        self.clear_irq_flags(RxDone=1)
        payload = self.read_payload(nocheck=True)
        print(bytes(payload).decode())
        self.set_mode(MODE.SLEEP)
        self.reset_ptr_rx()
        BOARD.led_off()
        self.set_mode(MODE.RXCONT)

    def on_tx_done(self):
        print("\nTxDone")
        print(self.get_irq_flags())

    def on_cad_done(self):
        print("\non_CadDone")
        print(self.get_irq_flags())

    def on_rx_timeout(self):
        print("\non_RxTimeout")
        print(self.get_irq_flags())

    def on_valid_header(self):
        print("\non_ValidHeader")
        print(self.get_irq_flags())

    def on_payload_crc_error(self):
        print("\non_PayloadCrcError")
        print(self.get_irq_flags())

    def on_fhss_change_channel(self):
        print("\non_FhssChangeChannel")
        print(self.get_irq_flags())

    def start(self):
        self.reset_ptr_rx()
        self.set_mode(MODE.RXCONT)
        while True:
            sleep(.5)
            rssi_value = self.get_rssi_value()
            status = self.get_modem_status()
            sys.stdout.flush()
            sys.stdout.write("\r%d %d %d" % (rssi_value, status['rx_ongoing'], status['modem_clear']))

def on_sigint(signum, frame):
    print('sigint')
    sys.exit(0)


def on_sigterm(signum, frame):
    print('sigterm')
    sys.exit(0)

if __name__ == '__main__':
#    signal.signal(signal.SIGINT, on_sigint)
#    signal.signal(signal.SIGTERM, on_sigterm)

    BOARD.setup()

    parser = LoRaArgumentParser("Continous LoRa receiver.")

    lora = LoRaGatewayService(board=BOARD, verbose=True, do_calibration=True, calibration_freq=433.3)
    args = parser.parse_args(lora)

    lora.set_mode(MODE.STDBY)
    lora.set_pa_config(pa_select=1)

    print(lora)
    assert(lora.get_agc_auto_on() == 1)

    try: input("Press enter to start...")
    except: pass

    try:
        lora.start()
    except KeyboardInterrupt:
        sys.stdout.flush()
        print("")
        sys.stderr.write("KeyboardInterrupt\n")
    finally:
        sys.stdout.flush()
        print("")
        lora.set_mode(MODE.SLEEP)
        print(lora)
        BOARD.teardown()

