from library.server import Server, Handler


class SimpleHandler(Handler):

    def process(self, request):
        decoded_request = bytes.decode(request, encoding='utf-8')
        rows = decoded_request.split("\r\n")
        path = rows[0]
        path_elements = path.split(" ")
        if path_elements[0] == 'GET' and path_elements[1] == '/':
            return self.prepare()

    def prepare(self):
        file = open("./index.html")
        page = str(file.read())
        file.close()

        response_headers = {
            'Content-Type': 'text/html; encoding=utf8',
            'Content-Length': len(page),
            'Connection': 'close',
        }

        response_headers_raw = ''.join('%s: %s\n' % (k, v) for k, v in response_headers.items())
        response_proto = 'HTTP/1.1'
        response_status = '200'
        response_status_text = 'OK'

        response = f"{response_proto}\n"
        response += f"{response_status}\n"
        response += f"{response_status_text}\n"
        response += f"{response_headers_raw}"
        response += f"\n"
        response += f"{page}"

        return bytes(response, encoding='utf-8')


def start_server():
    server = Server("127.0.0.1", 9090, SimpleHandler())
    server.start_listening()


if __name__ == "__main__":
    start_server()
