from method import Method_Enum

class Response():
    def __init__(self, server):
        self.server = server

    def handle_response(self, packet, addr):
        method = packet.split(' ', 1)[0]
        for e in Method_Enum:
            if method == e.name:
                func = getattr(self, method.lower())
                func(addr)

    def get(self, addr):
        # Send a "Hello" message for now
        self.server.send_to_connection(addr, 'HTTP/1.1 200 OK\r\nContent-Type:text/html\r\n\r\nHello')