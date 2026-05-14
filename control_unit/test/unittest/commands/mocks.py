
# ---------------------------------------------------------------------------------------------------------------------
from control_unit.control.interfaces.actor import Actor
from control_unit.control.interfaces.communication import Communicator, State

# ---------------------------------------------------------------------------------------------------------------------

class MockCom(Communicator):

    def __init__(self):
        pass

    def add_actor(self, name: str) -> None:
        pass

    def transmit_actor_state(self, state: State) -> None:
        pass

    def transmit_mode(self, mode: str) -> None:
        pass

    def transmit_generic_message(self, msg: str) -> None:
        pass
    pass

# ---------------------------------------------------------------------------------------------------------------------

class MockActor(Actor):

    def __init__(self, name: str):
        self.__name: str = name
        self.__state: bool = False
        pass

    def activate(self, flag: bool) -> None:
        self.__state = flag

    def state(self) -> bool:
        return self.__state

    def name(self) -> str:
        return self.__name
    pass
# ---------------------------------------------------------------------------------------------------------------------
