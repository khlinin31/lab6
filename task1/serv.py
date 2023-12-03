from library.server import Server, Handler


class SimpleHandler(Handler):

    def process(self, request):
        return request


def start_server():
    server = Server("127.0.0.1", 9090, SimpleHandler())
    server.start_listening()


if __name__ == "__main__":
    start_server()
