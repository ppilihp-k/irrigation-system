# ---------------------------------------------------------------------------------------------------------------------
from time import sleep

import machine  # pylint: disable=import-error
import network  # pylint: disable=import-error

from control_unit.config.wlan import WLAN_PASSWORD, WLAN_SSID

# ---------------------------------------------------------------------------------------------------------------------

__led_onboard: machine.Pin = machine.Pin("LED", machine.Pin.OUT, value=0)


def wlan_is_connected() -> bool:
    """Check if WLan Connection is working."""
    wlan: network.WLAN = network.WLAN(network.STA_IF)
    if wlan.isconnected():
        __led_onboard.on()
        return True
    __led_onboard.off()
    return False


def wlan_connect() -> None:
    """Connect to a WLAN Network."""
    wlan: network.WLAN = network.WLAN(network.STA_IF)
    if not wlan.isconnected():
        wlan.active(True)
        wlan.connect(WLAN_SSID, WLAN_PASSWORD)
        for _ in range(10):
            if wlan.status() < 0 or wlan.status() >= 3:
                break
            __led_onboard.toggle()
            sleep(1)
    if wlan.isconnected():
        __led_onboard.on()
    else:
        __led_onboard.off()

    pass


# ---------------------------------------------------------------------------------------------------------------------
