class request:
    def __init__(self) -> None:
        self.method = None
        self.path = None
        self.protocol = None
        self.headers = {}
        self.data = {}
        self.body = None

    def parse(self, string) -> None:
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
                 x.split(b"=") for x in (
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
        
    def compile(self) -> str:
        return self.method + b" " +  self.path + b"?" + b"&".join(["=".join([key, value]) for key, value in self.data["GET"].items()]) + b" " + self.protocol + b"\r\n" + b"\r\n".join([key + b": " + value for key, value in self.headers.items()]) + b"\r\n\r\n" + self.body