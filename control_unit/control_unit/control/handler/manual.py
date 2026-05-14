
# ---------------------------------------------------------------------------------------------------------------------
from control_unit.control.handler.interfaces import ModeHandler
from control_unit.control.interfaces.actor import Actor
from control_unit.control.interfaces.communication import Communicator
from control_unit.control.interfaces.logger import Logger

# ---------------------------------------------------------------------------------------------------------------------

class Handler(ModeHandler):

    def __init__(self, actors: list[Actor], logger: Logger):
        self.__actors: list[Actor] = actors
        self.__logger: Logger = logger
        pass

    def set_logger(self, logger: Logger) -> None:
        self.__logger = logger
        pass

    def _actor(self, name: str) -> Actor | None:
        for a in self.__actors:
            if a.name() == name:
                return a
        return None

    def handle_actuator_state_change_request(self, actuator: str, flag: bool) -> None:
        actor: Actor | None = self._actor(actuator)
        if actor is None:
            self.__logger.log(
                f'Unable to change Actor {actuator} State to {flag}. Actor not found.'
            )
            return
        actor.activate(flag)
        pass

    pass

# ---------------------------------------------------------------------------------------------------------------------
