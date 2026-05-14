# ---------------------------------------------------------------------------------------------------------------------
from control_unit.config.core import QUEUE_ITEM_SIZE
from control_unit.config.mqtt import (
    BASE_TOPIC,
    CLIENT_ID,
    MQTT_KEEP_ALIVE,
    PASSWORD,
    PORT,
    URL,
    USER_NAME,
)
from control_unit.control.interfaces.communication import (
    CommandReceiver,
    Communicator,
    CommunicatorPublishException,
    State,
)

from ._umqtt.simple import MQTTClient  # type: ignore[attr-defined]

# ---------------------------------------------------------------------------------------------------------------------


class MqttClient(Communicator):
    def __create_client(self) -> MQTTClient:
        mqttc: MQTTClient = MQTTClient(
            client_id=CLIENT_ID,
            server=URL,
            port=PORT,
            user=USER_NAME,
            password=PASSWORD,
            keepalive=MQTT_KEEP_ALIVE,
        )
        mqttc.set_callback(self.__on_message)
        mqttc.connect()

        mqttc.subscribe(f"{BASE_TOPIC}command/".encode())
        return mqttc

    def __init__(self) -> None:
        super().__init__()
        self.__message_queue: list[bytes] = []
        self.__output_queue: list[tuple[bytes, bytes]] = []
        self.__mqttc: MQTTClient | None = None
        pass

    def __del__(self) -> None:
        if self.__mqttc is not None:
            self.__mqttc.disconnect()
        pass

    def __on_message(self, topic: bytes, message: bytes) -> None:
        if topic.decode() == f"{BASE_TOPIC}command/":
            self.__message_queue.append(message)
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
        except Exception as e:  # pylint: disable=broad-exception-caught # Mqtt must not influence Hardware control Loop...
            print(e)
            print("Unable to read Messages!")

    #
    # ================ Communicator ===========================================
    #
    def add_actor(self, name: str) -> None:
        try:
            self.__output_queue.append(
                (
                    f"{BASE_TOPIC}".encode(),
                    name.encode(),
                )
            )
        except Exception as e:
            raise CommunicatorPublishException from e

        pass

    def transmit_actor_state(self, state: State) -> None:
        try:
            self.__output_queue.append(
                (
                    f"{BASE_TOPIC}{state.instance}".encode(),
                    str(int(state.active)).encode(),
                )
            )
        except Exception as e:
            raise CommunicatorPublishException from e
        pass

    def transmit_generic_message(self, msg: str) -> None:
        try:
            self.__output_queue.append(
                (
                    f"{BASE_TOPIC}generic".encode(),
                    msg.encode(),
                )
            )
        except Exception as e:
            raise CommunicatorPublishException from e
        pass

    pass


# ---------------------------------------------------------------------------------------------------------------------
