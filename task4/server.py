import socket
import logging
import threading


class Server(threading.Thread):

    def __init__(self, hostname='localhost', port=1337):
        super().__init__()
        self.connections = []
        self.host = hostname
        self.port = port

    def run(self):
        sock = socket.socket()
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind((self.host, self.port))

        sock.listen(1)
        print(f"Server started listening on {self.host}:{self.port}")
        logging.debug(f"Server started listening on {self.host}:{self.port}")

        while True:
            sc, hostname = sock.accept()
            print(f"Accept new connection from {sc.getpeername()}")
            logging.debug(f"Accept new connection from {sc.getpeername()}")

            server_socket = Connection(sc, hostname, self)
            server_socket.start()

            self.connections.append(server_socket)

    def broadcast(self, message, source):
        for connection in self.connections:
            if connection.client_name != source:
                connection.send(message)

    def remove_connection(self, connection):
        logging.debug(f"Remove connection {connection}")
        self.connections.remove(connection)

    def close(self):
        logging.debug("Shutting down server")
        for connection in self.connections:
            connection.sc.close()


class Connection(threading.Thread):

    def __init__(self, socket: socket.socket, client_name: str, server: Server):
        super().__init__()
        self.sc = socket
        self.client_name = client_name
        self.server = server

    def run(self):

        while True:
            message = self.sc.recv(2048).decode('utf-8')
            if message:
                print(f"Client '{self.client_name}' send message '{message}'")
                self.server.broadcast(message, self.client_name)
            else:
                print(f"Client '{self.client_name}' closed the connection")
                self.sc.close()
                self.server.remove_connection(self)
                return

    def send(self, message):
        self.sc.sendall(message.encode('utf-8'))


if __name__ == '__main__':
    server = Server()
    server.run()
