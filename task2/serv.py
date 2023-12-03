import math

from library.server import Server, Handler


class SimpleHandler(Handler):

    def process(self, request):
        decoded_request = bytes.decode(request, encoding="utf-8")
        args = decoded_request.split(";")
        coefficients = {}
        for arg in args:
            key, value = arg.split("=")
            coefficients[key] = value

        A = int(coefficients.get("A", 0))
        B = int(coefficients.get("B", 0))
        C = int(coefficients.get("C", 0))
        D = B**2 - 4*A*C

        answer = None
        if D < 0:
            answer = "This equation has no real solution"
        elif D == 0:
            x = (-B + math.sqrt(B ** 2 - 4 * A * C)) / 2 * A
            answer = f"This equation has one solutions: {x}"
        else:
            x1 = (-B + math.sqrt((B ** 2) - (4 * (A * C)))) / (2 * A)
            x2 = (-B - math.sqrt((B ** 2) - (4 * (A * C)))) / (2 * A)
            answer = f"This equation has two solutions: {x1} or {x2}"
        return bytes(answer, encoding='utf-8')


def start_server():
    server = Server("127.0.0.1", 9090, SimpleHandler())
    server.start_listening()


if __name__ == "__main__":
    start_server()
