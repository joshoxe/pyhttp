import socket, response_manager

class Server:
    # Server info
    server_name = 'pyhttp'
    http_version = 'HTTP/1.1'
    # Active connections (This could become more useful with threading)
    connections = {}

    def start_server(self):
        manager = response_manager.Response(self)
        with socket.socket() as sock:
            sock.bind(("127.0.0.1", 80))
            sock.listen(1)
            while True:
                conn, addr = sock.accept()
                self.add_connection(conn, addr)
                with conn:
                    packet = conn.recv(1024).decode('utf-8')
                    manager.handle_response(packet, addr)
                    self.remove_connection(addr)


    def add_connection(self, conn, addr):
        self.connections[addr] = conn

    def remove_connection(self, addr):
        del self.connections[addr]

    def send_to_connection(self, addr, packet):
        if addr in self.connections:
            self.connections[addr].send(packet.encode("ascii"))



pyhttp = Server()
pyhttp.start_server()