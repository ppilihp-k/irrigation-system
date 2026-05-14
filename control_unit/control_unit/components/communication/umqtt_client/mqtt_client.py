
# ---------------------------------------------------------------------------------------------------------------------
from control_unit.control.interfaces.communication import Communicator, State, CommunicatiorConnectionFailed, CommunicatorPublishException, CommandReceiver
from control_unit.control.core import Core
from control_unit.config.mqtt import URL, PORT, USER_NAME, PASSWORD, BASE_TOPIC, MQTT_KEEP_ALIVE, CLIENT_ID
from control_unit.config.core import QUEUE_ITEM_SIZE

from json import dumps

from ._umqtt.simple import MQTTClient, MQTTException
# ---------------------------------------------------------------------------------------------------------------------


class MqttClient(Communicator):

    def __create_client(self) -> MQTTClient:
        mqttc: MQTTClient = MQTTClient(
            client_id=CLIENT_ID, server=URL, port=PORT, user=USER_NAME, password=PASSWORD, keepalive=MQTT_KEEP_ALIVE,
        )
        mqttc.set_callback(self.__on_message)
        mqttc.connect()

        print(
            f'Subscribe to Topic {BASE_TOPIC}command/'
        )
        mqttc.subscribe(
            f'{BASE_TOPIC}command/'.encode()
        )
        return mqttc


    def __init__(self):
        super().__init__()
        self.__message_queue = []
        self.__output_queue = []
        self.__mqttc: MQTTClient | None = None
        pass

    def __del__(self):
        if self.__mqttc is not None:
            self.__mqttc.disconnect()
        pass

    def __on_message(self, topic: bytes, message: bytes):
        print(f'UMQTT: Received msg on Topic {topic}')
        if topic.decode() == f'{BASE_TOPIC}command/':
            self.__message_queue.append(message)
            print(f'Pushed {message} to Queue...')
        pass

    def dispatch(self, receiver: CommandReceiver) -> None:
        try:
            if self.__mqttc is None:
                self.__mqttc = self.__create_client()
            self.__mqttc.ping()
            while len(self.__output_queue) > 0:
                t = self.__output_queue.pop(0)
                self.__mqttc.publish(
                    t[0],
                    t[1],
                )

            buffer: bytearray = bytearray(QUEUE_ITEM_SIZE)
            self.__mqttc.check_msg()
            while len(self.__message_queue) > 0:
                msg: bytes = self.__message_queue.pop(0)
                receiver.command(msg, buffer)
        except Exception as e:
            print(e)
            print('Unable to read Messages!')

    #
    # ================ Communicator ===========================================
    #
    def add_actor(self, name: str) -> None:
        try:
            self.__output_queue.append(
                (f'{BASE_TOPIC}'.encode(), name.encode(),)
            )
        except Exception as e:
            raise CommunicatorPublishException from e

        pass

    def transmit_actor_state(self, state: State) -> None:
        try:
            self.__output_queue.append(
                (f'{BASE_TOPIC}{state.instance}'.encode(), str(int(state.active)).encode(),)
            )
        except Exception as e:
            raise CommunicatorPublishException from e
        pass

    def transmit_generic_message(self, msg: str) -> None:
        try:
            self.__output_queue.append(
                (f'{BASE_TOPIC}generic'.encode(), msg.encode(),)
            )
        except Exception as e:
            raise CommunicatorPublishException from e
        pass

    pass
# ---------------------------------------------------------------------------------------------------------------------
