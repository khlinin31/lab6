from library.client import Client


def start_client():
    client = Client("127.0.0.1", 9090)
    client.start_connection()
    client.send("Hello, server")
    response = bytes.decode(client.receive())
    print(response)


if __name__ == "__main__":
    start_client()
