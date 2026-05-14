
# ---------------------------------------------------------------------------------------------------------------------
from unittest import TestCase
from unittest.mock import MagicMock
from control_unit.control.core import Core
from control_unit.control.interfaces.actor import Actor
from control_unit.control.interfaces.communication import Communicator, State

from control_unit.config.core import QUEUE_ITEM_SIZE
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


class TestCore(TestCase):

    def test_initial(self):
        core: Core = Core()
        pass

    def test_actuator_command(self):
        actor: MockActor = MockActor('valve0')
        core: Core = Core()

        com: MockCom = MockCom()
        core.set_communicator(com)

        core.add_actor(actor)

        buffer: bytearray = bytearray(QUEUE_ITEM_SIZE)
        core.actor_command(
            b'valve0', b'1', buffer
        )
        core.dispatch()
        self.assertTrue(
            actor.state(),
        )
        core.actor_command(
            b'valve0', b'0', buffer
        )
        core.dispatch()
        self.assertFalse(
            actor.state(),
        )
        pass

    def test_core_command(self):
        actor: MockActor = MockActor('valve0')
        core: Core = Core()

        com: MockCom = MockCom()
        core.set_communicator(com)

        core.add_actor(actor)

        buffer: bytearray = bytearray(QUEUE_ITEM_SIZE)
        core.command(b'test', buffer)
        core.dispatch()
        pass

    pass

# ---------------------------------------------------------------------------------------------------------------------
