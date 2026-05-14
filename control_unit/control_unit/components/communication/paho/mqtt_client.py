
# ---------------------------------------------------------------------------------------------------------------------
from control_unit.control.interfaces.communication import Communicator, State, CommandReceiver
from control_unit.control.core import Core
from control_unit.config.mqtt import URL, PORT, USER_NAME, PASSWORD, BASE_TOPIC
from control_unit.config.core import QUEUE_ITEM_SIZE

from json import dumps

import paho.mqtt.client as mqtt


# ---------------------------------------------------------------------------------------------------------------------

class MqttClient(Communicator):

    def __init__(self):
        super().__init__()
        self.__mqttc = None
        mqttc: mqtt.Client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
        mqttc.on_connect = self.on_connect
        mqttc.on_message = self.on_message
        mqttc.connect(URL, PORT, 60)

        mqttc.subscribe(
            f'{BASE_TOPIC}command/'
        )

        mqttc.loop_start()
        self.__mqttc = mqttc

        self.__message_queue = []

        pass

    def __del__(self):
        if self.__mqttc is not None:
            self.__mqttc.loop_stop()

    def on_connect(self, *args, **kwargs):
        pass

    def on_message(self, client, userdata, message):
        try:
            if message.topic == f'{BASE_TOPIC}command/':
                #self.__core.command(message.payload, buffer)
                self.__message_queue.append(message.payload)
        except Exception as e:
            print(e)
        pass

    def dispatch(self, receiver: CommandReceiver) -> None:
        buffer: bytearray = bytearray(QUEUE_ITEM_SIZE)
        while len(self.__message_queue) > 0:
            msg: bytes = self.__message_queue.pop(0)
            receiver.command(
                msg, buffer,
            )
        pass

    #
    # ================ Communicator ===========================================
    #
    def add_actor(self, message: str) -> None:
        self.__mqttc.publish(
            f'{BASE_TOPIC}', message,
        )
        print('transmit add actor')
        pass

    def transmit_actor_state(self, state: State) -> None:
        print(f'{BASE_TOPIC}{state.instance}: {state.active}')
        self.__mqttc.publish(
            f'{BASE_TOPIC}{state.instance}', int(state.active),
        )
        print('transmit actor state')
        pass

    def transmit_generic_message(self, msg: str) -> None:
        self.__mqttc.publish(
            f'{BASE_TOPIC}generic',
            msg
        )
        pass

    pass
# ---------------------------------------------------------------------------------------------------------------------
