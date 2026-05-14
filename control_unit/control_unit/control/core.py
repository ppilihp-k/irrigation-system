# ---------------------------------------------------------------------------------------------------------------------
from json import dumps, loads

from control_unit.config.core import (
    MESSAGE_MAX_SIZE,
    NAME_MAX_SIZE,
    QUEUE_CAPACITY,
    QUEUE_ITEM_SIZE,
    TOKEN_SIZE,
)
from control_unit.control.handler.interfaces import ModeHandler
from control_unit.control.handler.manual import Handler as ManualHandler
from control_unit.control.interfaces.actor import Actor
from control_unit.control.interfaces.communication import (
    CommandReceiver,
    Communicator,
    CommunicatorPublishException,
    State,
)
from control_unit.control.interfaces.logger import Logger
from control_unit.control.logger.com_logger import ComLogger
from control_unit.queue.queue import Queue

try:
    from time import (  # type: ignore[attr-defined] # Defined for micropython on pico
        ticks_ms,
    )
except ImportError:
    from time import time_ns

    def ticks_ms() -> int:
        return time_ns() // 1000


# ---------------------------------------------------------------------------------------------------------------------

CORE = 0
ACTOR = 1
CLOCK = 2

# ---------------------------------------------------------------------------------------------------------------------


class VoidLogger(Logger):  # pylint: disable=too-few-public-methods # Dummyclass for default initialization.
    def log(self, msg: str) -> None:
        pass

    pass


# ---------------------------------------------------------------------------------------------------------------------


class VoidCommunicator(Communicator):
    def add_actor(self, name: str) -> None:
        pass

    def transmit_actor_state(self, state: State) -> None:
        pass

    def transmit_generic_message(self, msg: str) -> None:
        pass

    pass


# ---------------------------------------------------------------------------------------------------------------------


class Core(CommandReceiver):
    """Public Functions have to be Interruptsave."""

    def __init__(
        self,
    ) -> None:
        self.__com: Communicator = VoidCommunicator()
        self.__logger: Logger = VoidLogger()
        # create a Handler...
        self.__actors: list[Actor] = []
        self.__manual_handler = ManualHandler(
            self.__actors,
            self.__logger,
        )
        self.__current_handler: ModeHandler = self.__manual_handler
        self.__input_queue: Queue = Queue(capacity=QUEUE_CAPACITY, max_item_size=QUEUE_ITEM_SIZE)
        self.__ticks_last_update: int = 0
        pass

    def actuator(self) -> list[str]:
        return [a.name() for a in self.__actors]

    def set_communicator(self, com: Communicator) -> None:
        """Set Communicator.

        Not IRQ save.
        """
        self.__com = com
        self.__logger = ComLogger(com)
        self.__manual_handler.set_logger(self.__logger)
        for actor in self.__actors:
            self.__com.transmit_actor_state(
                State(
                    instance=actor.name(),
                    active=actor.state(),
                )
            )
        pass

    def add_actor(self, actor: Actor) -> None:
        """Add an Actor.

        Not IRQ save.
        """
        self.__actors.append(actor)
        self.__com.add_actor(
            dumps(
                {
                    "actuators": self.actuator(),
                }
            )
        )
        self.__com.transmit_actor_state(
            State(
                instance=actor.name(),
                active=actor.state(),
            )
        )
        pass

    def command(self, msg: bytes, buffer: bytearray) -> None:
        """Send a Command to the Core.

        IRQ save.

        Args:
            msg: bytes: The Message to be send.
            buffer: bytearray: The Caller has to allocate the Memory.
                This Function will then create a Message within the given Buffer.
                After the Function returns the Caller can deallocate the Buffer.
        """
        buffer[0 : len(buffer)] = b"\0" * len(buffer)
        buffer[0:1] = CORE.to_bytes(1)  # 0             -- 1                            = Type
        buffer[1 : 1 + len(msg)] = msg
        self.__input_queue.enqueue(bytes(buffer))
        pass

    def actor_command(self, name: bytes, msg: bytes, buffer: bytearray) -> None:
        buffer[0 : len(buffer)] = b"\0" * len(buffer)
        buffer[0:1] = ACTOR.to_bytes(1)  # 0             -- 1                            = Type
        buffer[1 : 1 + NAME_MAX_SIZE] = name[0:NAME_MAX_SIZE]  # 1             -- 1 + NAME_SIZE                = Name
        buffer[
            1 + NAME_MAX_SIZE : 1 + NAME_MAX_SIZE + MESSAGE_MAX_SIZE
        ] = msg  # 1 + NAME_SIZE -- 1 + NAME_SIZE + MESSAGE_SIZE = Message
        self.__input_queue.enqueue(bytes(buffer))
        pass

    def clock_alarm(self, buffer: bytearray) -> None:
        buffer[0 : len(buffer)] = b"\0" * len(buffer)
        buffer[0:1] = CLOCK.to_bytes(1)
        self.__input_queue.enqueue(bytes(buffer))
        pass

    def decode_actor_command(self, msg: bytes) -> tuple[str, str]:
        return (
            msg[TOKEN_SIZE : TOKEN_SIZE + NAME_MAX_SIZE].decode().rstrip("\0"),  # 0 -- 8
            msg[TOKEN_SIZE + NAME_MAX_SIZE : TOKEN_SIZE + NAME_MAX_SIZE + MESSAGE_MAX_SIZE]  # 8 -- 64
            .decode()
            .rstrip("\0"),
        )

    def decode_command(self, msg: bytes) -> str:
        return msg[1 : len(msg)].decode().rstrip("\0")

    def _handle_actor_command(self, actor: str, data: str) -> None:
        state: bool = False
        try:
            new_state: int = int(data)
            if new_state != 0:
                state = True
            self.__current_handler.handle_actuator_state_change_request(
                actor,
                state,
            )
        except Exception as e:  # pylint: disable=broad-exception-caught # Just reset the Actor State..
            print(e)
            self.__current_handler.handle_actuator_state_change_request(
                actor,
                False,
            )
        pass

    def _handle_clock(self) -> None:
        pass

    CORE_COMMAND_SET_ACTOR_STATE: str = "set_actor_state"

    def _handle_command(self, msg: str) -> None:
        """

        {
            "command": str,
            "data": ...
        }
        """
        try:
            command = loads(msg)
            print(f"Process Command {msg}")
            command_name: str = command["command"]
            if self.CORE_COMMAND_SET_ACTOR_STATE == command_name:
                state = int(command["data"]["state"])
                actor_name = str(command["data"]["actor"])
                self.__current_handler.handle_actuator_state_change_request(
                    actor_name,
                    bool(state),
                )
                self.__com.transmit_actor_state(
                    State(
                        instance=actor_name,
                        active=bool(state),
                    )
                )
        except CommunicatorPublishException:
            print("Unable to Publisch Message!")
        except KeyError:
            self.__logger.log("Wrong Schema!")
        except ValueError:
            self.__logger.log(f"JSONDecodeError: {msg}")
            pass
        pass

    def dispatch(self) -> None:
        """Dispatch a Command."""
        try:
            try:
                current_ticks: int = ticks_ms()
                last_ticks: int = self.__ticks_last_update
                if (current_ticks - last_ticks) > 1000:
                    self.__ticks_last_update = current_ticks
                    self.__com.add_actor(
                        dumps(
                            {
                                "actuators": self.actuator(),
                            }
                        )
                    )
                    for a in self.__actors:
                        self.__com.transmit_actor_state(State(instance=a.name(), active=a.state()))
            except CommunicatorPublishException:
                print("Dispatch: Unable to publish Actor States.")

            output: bytearray = bytearray(QUEUE_ITEM_SIZE)
            while self.__input_queue.dequeue(output):
                if ACTOR == int(output[0]):
                    values: tuple[str, str] = self.decode_actor_command(bytes(output))
                    self._handle_actor_command(values[0], values[1])
                elif CLOCK == int(output[0]):
                    self._handle_clock()
                elif CORE == int(output[0]):
                    self._handle_command(
                        self.decode_command(bytes(output)),
                    )
                else:
                    self.__logger.log("Unknown Message!")
            self.__current_handler.handle_tick()
        except Exception as e:  # pylint: disable=broad-exception-caught
            print(f"Core.dispatch: {e}")

        pass

    pass


# ---------------------------------------------------------------------------------------------------------------------
