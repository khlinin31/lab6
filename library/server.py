import socket
from abc import ABC, abstractmethod

MAX_PACKET = 32768


class Handler(ABC):

    @abstractmethod
    def process(self, request):
        pass


class Server:

    def __init__(self, hostname: str, port: int, handler: Handler) -> None:
        super().__init__()
        self._socket = socket.socket()
        self._hostname = hostname
        self._port = port
        self._handler = handler
        self._opened = True

    def start_listening(self):
        self._socket.bind((self._hostname, self._port))

        self._socket.listen()

        while self._opened:
            try:
                connection, address = self._socket.accept()

                print(f"{address} connected")

                rdata = []
                while True:
                    data = connection.recv(MAX_PACKET)
                    if not data:
                        break
                    rdata.append(data)
                    if data.__sizeof__() * 8 < MAX_PACKET:
                        break

                connection.send(self._handler.process(b''.join(rdata)))
            except Exception as ex:
                print(f"connection error\n{ex}")

        self.close()

    def close(self):
        self._socket.close()
