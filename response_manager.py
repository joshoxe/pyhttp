import datetime, resource_handler, collections, response
from method import MethodEnum
from wsgiref.handlers import format_date_time
from time import mktime

class Response():
    def __init__(self, server):
        self.server = server
        self.struct = collections.namedtuple('data', ('method', 'path'))
        self.resource = resource_handler.Resource()
        self.response_codes = response.ResponseCodes().respone

    def handle_response(self, packet, addr):
        # TODO: All kinds of error handling
        # TODO: Re-write how we handle response codes (and get them!) which will make error handling much more simple
        split = packet.split(' ')
        path = split[1]
        # Replace "/" with "/index.html"
        if path == "/":
            path = "/index.html"
        data = self.struct(split[0], path)
        for e in MethodEnum:
            if data.method == e.name:
                func = getattr(self, data.method.lower())
                func(addr, data)

    def get(self, addr, data):
        self.server.send_to_connection(addr, self.response_builder(data.path))

    def response_builder(self, file):
        # TODO: Not sure how to handle other methods yet, but maybe have a switch(method) condition in here
        packet = ""
        response = ""
        # Does file exist
        try:
            content = self.resource.read_file(file)
            response = ResponseEnum.OK
        except FileNotFoundError:
            response = ResponseEnum.NOT_FOUND
            # Peronal 404 responses? Save for config
            content = ""
        packet += "{} {}".format(self.server.http_version, self.get_status(response))
        # Get the headers. Currently supporting basic static headers
        # TODO: A way to send these dynamically based on request headers. Possibly an enum? Receive a string request header and find the corresponding response
        headers = {}
        headers["Date"] = self.current_date()
        headers["Server"] = self.server.server_name
        headers["Content-Type"] = self.resource.get_content_type(file)[0]

        for header in headers:
            packet += "\r\n{}: {}".format(header, headers[header])
        packet += "\r\n\r\n{}".format(content)
        print(packet)
        return packet

    def current_date(self):
        return format_date_time(mktime(datetime.datetime.now().timetuple()))

    def get_status(self, enum):
        return "{} {}".format(enum.value, str(enum.name).replace("_", " "))
