import mimetypes
class Resource():

    def read_file(self, file):
        with open("www" + file, 'r') as f:
            return f.read()

    def get_content_type(self, file):
        return mimetypes.guess_type(file)
