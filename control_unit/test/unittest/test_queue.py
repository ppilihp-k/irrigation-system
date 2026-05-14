
# ---------------------------------------------------------------------------------------------------------------------
from unittest import TestCase
from control_unit.queue.queue import Queue

# ---------------------------------------------------------------------------------------------------------------------


class TestQueue(TestCase):

    def test_initial(self) -> None:
        q: Queue = Queue(capacity=4, max_item_size=32)

        pass

    def test_enqueue_n(self) -> None:
        q: Queue = Queue(capacity=4, max_item_size=32)
        list_of_bytes: list[bytes] = [
            b'0' * 31 + b'1',
            b'0' * 31 + b'2',
            b'0' * 31 + b'3',
            b'0' * 31 + b'4',
        ]
        for b in list_of_bytes:
            q.enqueue(
                b
            )
        self.assertEqual(
            b'0' * 31 + b'1' + b'0' * 31 + b'2' + b'0' * 31 + b'3' + b'0' * 31 + b'4',
            q.data()
        )
        pass

    def test_enqueue_n_plus_one(self) -> None:
        q: Queue = Queue(capacity=4, max_item_size=32)
        list_of_bytes: list[bytes] = [
            b'0' * 31 + b'1',
            b'0' * 31 + b'2',
            b'0' * 31 + b'3',
            b'0' * 31 + b'4',
            b'0' * 31 + b'5',
        ]
        for b in list_of_bytes:
            q.enqueue(
                b
            )
        self.assertEqual(
            b'0' * 31 + b'1' + b'0' * 31 + b'2' + b'0' * 31 + b'3' + b'0' * 31 + b'4',
            q.data()
        )
        pass


    def test_dequeue_on_empty_queue(self) -> None:
        q: Queue = Queue(capacity=4, max_item_size=32)
        output: bytearray = bytearray(32)
        self.assertFalse(
            q.dequeue(output)
        )
        pass

    def test_dequeue_n(self) -> None:
        q: Queue = Queue(capacity=4, max_item_size=32)
        list_of_bytes: list[bytes] = [
            b'0' * 31 + b'1',
            b'0' * 31 + b'2',
            b'0' * 31 + b'3',
            b'0' * 31 + b'4',
        ]
        for b in list_of_bytes:
            q.enqueue(b)
        output: bytearray = bytearray(32)
        for i in range(len(list_of_bytes)):
            self.assertTrue(
                q.dequeue(output)
            )
            self.assertEqual(
                list_of_bytes[i],
                output,
            )
        self.assertFalse(
            q.dequeue(output)
        )

    pass

# ---------------------------------------------------------------------------------------------------------------------

