
# ---------------------------------------------------------------------------------------------------------------------
from control_unit.control.interfaces.logger import Logger
from control_unit.control.interfaces.communication import Communicator

# ---------------------------------------------------------------------------------------------------------------------

class ComLogger(Logger):

    def __init__(self, com: Communicator):
        self.__com: Communicator = com
        pass

    def log(self, msg: str) -> None:
        try:
            self.__com.transmit_generic_message(msg)
        except:
            pass
        pass
    pass
# ---------------------------------------------------------------------------------------------------------------------
