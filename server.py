import socket, response_manager, datetime
from wsgiref.handlers import format_date_time
from time import mktime

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
                    try:
                    packet = conn.recv(1024).decode('utf-8')
                    print("RECV:\r\n{}".format(packet))
                    manager.handle_response(packet, addr)
                    except Exception as e:
                        print(e)
                        self.send_to_connection(addr, "{} 500 Internal Server Error\r\n{}\r\n{}".format(self.http_version, self.current_date(), self.server_name))
                    self.remove_connection(addr)


    def add_connection(self, conn, addr):
        self.connections[addr] = conn

    def remove_connection(self, addr):
        del self.connections[addr]

    def send_to_connection(self, addr, packet):
        if addr in self.connections:
            print("SENT:\r\n{}".format(packet))
            self.connections[addr].send(packet.encode("ascii"))

    def current_date(self):
        return format_date_time(mktime(datetime.datetime.now().timetuple()))

pyhttp = Server()
pyhttp.start_server()