
# ---------------------------------------------------------------------------------------------------------------------
from unittest import TestCase
from unittest.mock import MagicMock
from control_unit.control.core import Core

from control_unit.config.core import QUEUE_ITEM_SIZE

from control_unit.control.interfaces.actor import Actor
from control_unit.control.interfaces.communication import Communicator, State

from .mocks import MockCom, MockActor
# ---------------------------------------------------------------------------------------------------------------------


class TestActorCommand(TestCase):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__actor: Actor | None = None
        self.__core: Core | None = None
        pass

    def setUp(self) -> None:
        self.__actor: MockActor = MockActor('valve0')
        self.__core: Core = Core()
        com: MockCom = MockCom()
        self.__core.set_communicator(com)
        self.__core.add_actor(self.__actor)
        pass

    def test_actuator_command(self):
        buffer: bytearray = bytearray(QUEUE_ITEM_SIZE)
        self.__core.actor_command(
            b'valve0', b'1', buffer
        )
        self.__core.dispatch()
        self.assertTrue(
            self.__actor.state(),
        )
        self.__core.actor_command(
            b'valve0', b'0', buffer
        )
        self.__core.dispatch()
        self.assertFalse(
            self.__actor.state(),
        )
        pass


    pass
# ---------------------------------------------------------------------------------------------------------------------
