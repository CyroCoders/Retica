class response:
    """ A Response Object
    
    :rtype: Response
    """
    def __init__(self):
        """ Initialize the Response Object.

        :rtype: Response
        """
        self.status = "200"
        self.headers = {}
        self.body = "Hello From Retica"
        self.protocol = "HTTP/1.1"
        self.content_type = "text/html"
        self.content_length = len(self.body)
        self.connection = "close"

    def parse(self, string) -> None:
        """ Parse a response from a string and set the attributes of the response object.

            :param string: The Encoded Response String (Bytes).
            :type string: bytes

            :rtype: None
        """
        lines = string.split("\r\n")
        self.protocol, self.status = lines[0].split(" ")
        for line in lines[1:]:
            if line == "":
                break
            key, value = line.split(": ")
            self.headers[key] = value
        self.body = "\r\n".join(lines[len(lines)-1:])

    def compile(self) -> bytes:
        """ Compile the response into a string.
        
            :rtype: bytes
        """
        self.content_length = len(self.body)
        self.headers["Content-Type"] = self.content_type
        self.headers["Content-Length"] = str(self.content_length)
        self.headers["Connection"] = self.connection
        return (self.protocol + " " + self.status + "\r\n" + "\r\n".join([key + ": " + value for key, value in self.headers.items()]) + "\r\n\r\n" + self.body).encode()