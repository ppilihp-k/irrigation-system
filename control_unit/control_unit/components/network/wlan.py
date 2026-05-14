
# ---------------------------------------------------------------------------------------------------------------------
import network
import machine
from control_unit.config.wlan import WLAN_PASSWORD, WLAN_SSID
from time import sleep
# ---------------------------------------------------------------------------------------------------------------------

__led_onboard: machine.Pin = machine.Pin('LED', machine.Pin.OUT, value=0)

def wlan_is_connected() -> bool:
    """Check if WLan Connection is working."""
    global __led_onboard
    wlan: network.WLAN = network.WLAN(network.STA_IF)
    if wlan.isconnected():
        __led_onboard.on()
        return True
    __led_onboard.off()
    return False

def wlan_connect():
    """Connect to a WLAN Network."""
    global __led_onboard
    wlan: network.WLAN = network.WLAN(network.STA_IF)
    if not wlan.isconnected():
        wlan.active(True)
        wlan.connect(WLAN_SSID, WLAN_PASSWORD)
        for i in range(10):
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
