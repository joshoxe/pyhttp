import mimetypes
class Resource():

    def try_file(self, file):
        try:
            f = open("www"+file)
        except FileNotFoundError:
            return 404
        except PermissionError:
            return 403
        finally:
            f.close()
        return True

    def read_file(self, file):
        with open("www" + file, 'r') as f:
            return f.read()

    def get_content_type(self, file):
        return mimetypes.guess_type(file)
