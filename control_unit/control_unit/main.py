# ---------------------------------------------------------------------------------------------------------------------
# from control_unit.components.communication.paho.mqtt_client import MqttClient
from control_unit.components.actor.gpio import GpioActor
from control_unit.components.communication.umqtt_client.mqtt_client import MqttClient
from control_unit.components.network.wlan import wlan_connect, wlan_is_connected
from control_unit.control.core import Core

# ---------------------------------------------------------------------------------------------------------------------

#
# Initialize Hardware
#
valve_0: GpioActor = GpioActor("valve_0", 0)
valve_1: GpioActor = GpioActor("valve_1", 1)
valve_2: GpioActor = GpioActor("valve_2", 2)

core: Core = Core()
mqtt_client: MqttClient = MqttClient()

#
# Set Mqtt Client.
#
core.set_communicator(mqtt_client)
#
# Add available Actuators.
#
core.add_actor(valve_0)
core.add_actor(valve_1)
core.add_actor(valve_2)
#
# Start the main loop.
#
while True:
    if not wlan_is_connected():
        wlan_connect()
    mqtt_client.dispatch(core)
    core.dispatch()
    pass

# ---------------------------------------------------------------------------------------------------------------------
