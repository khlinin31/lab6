import socket


class Client:

    def __init__(self, hostname: str, port: int) -> None:
        super().__init__()
        self._socket = socket.socket()
        self._hostname = hostname
        self._port = port

    def start_connection(self):
        self._socket.connect((self._hostname, self._port))

    def send(self, request):
        self._socket.send(bytes(request, encoding='utf-8'))

    def receive(self):
        return self._socket.recv(1024)

    def close(self):
        self._socket.close()
