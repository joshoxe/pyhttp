import resource_handler, collections, response, method

class Response():
    def __init__(self, server):
        self.server = server
        self.struct = collections.namedtuple('data', ('method', 'path'))
        self.resource = resource_handler.Resource()
        self.response_codes = response.ResponseCodes().respone
        self.methods = method.Method.methods

    def handle_response(self, packet, addr):
        response = {}
        try:
            split = packet.split(' ')
            path = split[1]
            # Redirect to index.html
            if path == "/":
                path = "/index.html"
            data = self.struct(split[0], path)
        except IndexError:
            self.server.send_to_connection(addr, "{} 400 {}\r\n{}\r\n{}".format(self.server.http_version, self.response_codes[400], self.server.current_date(), self.server.server_name))
            return
        if data.method in self.methods:
            func = getattr(self, data.method.lower())
            func(addr, response, data)
        else:
            self.server.send_to_connection(addr, "{} 405 {}\r\n{}\r\n{}".format(self.server.http_version, self.response_codes[405], self.server.current_date(), self.server.server_name))
            return

    def get(self, addr, response, data):
        packet = ""
        response = ""
        content = ""
        # Does file exist
        file_status = self.resource.try_file(data.path)
        if file_status is True:
            response = self.response_codes[200]
            content = self.resource.read_file(data.path)
        else:
            response = self.response_codes[file_status]

        packet += "{} {}".format(self.server.http_version, self.get_status(response))

        # Get the headers. Currently supporting basic static headers
        # TODO: A way to send these dynamically based on request headers. Possibly an enum? Receive a string request header and find the corresponding response
        headers = {}
        headers["Date"] = self.server.current_date()
        headers["Server"] = self.server.server_name
        headers["Content-Type"] = self.resource.get_content_type(data.path)[0]
        for header in headers:
            packet += "\r\n{}: {}".format(header, headers[header])
        packet += "\r\n\r\n{}".format(content)

        self.server.send_to_connection(addr, packet)

    def get_status(self, response):
        for key in self.response_codes:
            if self.response_codes[key] == response:
                return "{} {}".format(key, response)