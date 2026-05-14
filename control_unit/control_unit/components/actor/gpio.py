
# ---------------------------------------------------------------------------------------------------------------------

from control_unit.control.interfaces.actor import Actor

# ---------------------------------------------------------------------------------------------------------------------

class GpioActor(Actor):

    def __init__(self, name: str, pin: int):
        self.__name = name
        self.__state: bool = False
        pass

    def name(self) -> str:
        return self.__name

    def activate(self, flag: bool) -> None:
        self.__state = flag
        pass

    def state(self) -> bool:
        return self.__state

    pass

# ---------------------------------------------------------------------------------------------------------------------
