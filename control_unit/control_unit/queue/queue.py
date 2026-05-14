

# ---------------------------------------------------------------------------------------------------------------------

class Queue:

    def __init__(self, capacity: int, max_item_size: int):
        self.__max_item_size: int = max_item_size
        self.__capacity: int = capacity
        self.__size: int = 0
        self.__current_write_index: int = 0
        self.__current_read_index: int = 0
        self.__data: bytearray = bytearray(capacity * max_item_size)
        pass

    def empty(self) -> bool:
        return 0 == self.__size

    def full(self) -> bool:
        return self.__capacity == self.__size

    def enqueue(self, data: bytes) -> bool:
        if len(data) > self.__max_item_size:
            return False
        if self.full():
            return False
        self.__size = self.__size + 1
        self.__data[self.__current_write_index * self.__max_item_size: self.__current_write_index * self.__max_item_size + len(data)] = data
        self.__current_write_index = (self.__current_write_index + 1) % self.__capacity
        return True

    def dequeue(self, output: bytearray) -> bool:
        if len(output) < self.__max_item_size:
            return False
        if self.empty():
            return False
        self.__size = self.__size - 1
        output[0: self.__max_item_size] = self.__data[self.__current_read_index * self.__max_item_size: (self.__current_read_index + 1)* self.__max_item_size]
        self.__current_read_index = (self.__current_read_index + 1) % self.__capacity
        return True

    def data(self) -> bytes:
        return bytes(self.__data)

    pass

# ---------------------------------------------------------------------------------------------------------------------
