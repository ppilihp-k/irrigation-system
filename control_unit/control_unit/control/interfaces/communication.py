# ---------------------------------------------------------------------------------------------------------------------
class CommunicatorException(Exception):
    pass


class CommunicatiorConnectionFailed(CommunicatorException):
    pass


class CommunicatorPublishException(CommunicatorException):
    pass


class CommunicatorReadMessageException(CommunicatorException):
    pass


# ---------------------------------------------------------------------------------------------------------------------
class CommandReceiver:  # pylint: disable=too-few-public-methods # Simulate abstract Class...
    def command(
        self, msg: bytes, buffer: bytearray
    ) -> None:  # pylint: disable=unused-argument # Simulate abstract Class...
        pass

    pass


# ---------------------------------------------------------------------------------------------------------------------


class State:  # pylint: disable=too-few-public-methods # Simulate Dataclass.
    def __init__(self, instance: str, active: bool) -> None:
        self.instance: str = instance
        self.active: bool = active
        pass

    pass


# ---------------------------------------------------------------------------------------------------------------------


class Communicator:
    def add_actor(self, name: str) -> None:
        pass

    def transmit_actor_state(self, state: State) -> None:
        pass

    def transmit_generic_message(self, msg: str) -> None:
        pass

    pass


# ---------------------------------------------------------------------------------------------------------------------
