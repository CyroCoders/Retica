class request:
    """ A Request Object
    
    :param method: The HTTP Method.
    :type method: str
    :param path: The path of the request.
    :type path: str
    :param protocol: The protocol of the request.
    :type protocol: str
    :param headers: The headers of the request.
    :type headers: dict
    :param data: The data of the request.
    :type data: dict
    :param body: The body of the request.
    :type body: bytes
    
    :rtype: Request
    """
    def __init__(self):
        """ Initialize the request object.

        :rtype: Request
        """
        self.method = None
        self.path = None
        self.protocol = None
        self.headers = {}
        self.data = {}
        self.body = None

    def parse(self, string: bytes) -> None:
        """ Parse a request from a string and set the attributes of the request object.
        
        :param string: The Encoded Request String (Bytes).
        :type string: bytes
        
        :rtype: None
        """
        lines = string.split(b"\r\n")
        self.method, self.path, self.protocol = lines[0].split(b" ")
        for line in lines[1:]:
            if line == b"":
                break
            key, value = line.split(b": ")
            self.headers[key] = value
        self.body = b"\r\n".join(lines[len(lines)-1:])

        self.data["GET"] = {
            key.decode(): value.decode()
            for key, value in [
                x.split(b"=") if type(x) != int else (f"{x}".encode(),f"{x}".encode()) for x in (
                    self.path.split(b"?")[1].split(b"&") if b"&" in self.path.split(b"?")[1] else self.path.split(b"?")[1]
                )
            ]
        } if b"?" in self.path else {}

        self.data["POST"] = {
            key.decode(): value.decode()
            for key, value in [
                x.split(b"=") for x in (
                    self.body.split(b"&") if b"&" in self.body else self.body
                )
            ]
        } if self.method.upper() == b"POST" else {}

        self.data["COOKIE"] = {
            key.decode(): value.decode()
            for key, value in [
                (x.split(b"=")[0],b"=".join(x.split(b"=")[1:])) for x in (
                    self.headers[b"Cookie"].split(b"; ") if b"; " in self.headers[b"Cookie"] else [self.headers[b"Cookie"]]
                )
            ]
        } if b"Cookie" in self.headers else {}

        self.path = self.path.split(b"?")[0] if b"?" in self.path else self.path
        
    def compile(self) -> bytes:
        """ Compile the request into a string.

            :rtpye: bytes
        """
        return self.method + b" " +  self.path + b"?" + b"&".join(["=".join([key, value]) for key, value in self.data["GET"].items()]) + b" " + self.protocol + b"\r\n" + b"\r\n".join([key + b": " + value for key, value in self.headers.items()]) + b"\r\n\r\n" + self.body