class request:
    def __init__(self, string) -> None:
        self.string = string
        self.method = None
        self.path = None
        self.protocol = None
        self.headers = {}
        self.data = {}
        self.body = None

    def parse(self) -> None:
        lines = self.string.split("\r\n")
        self.method, self.path, self.protocol = lines[0].split(" ")
        for line in lines[1:]:
            if line == "":
                break
            key, value = line.split(": ")
            self.headers[key] = value
        self.body = "\r\n".join(lines[len(lines)-1:])

        self.data["GET"] = {
            key: value
            for key, value in [
                 x.split("=") for x in (
                     self.path.split("?")[1].split("&") if "&" in self.path.split("?")[1] else self.path.split("?")[1]
                )
            ]
        } if "?" in self.path else {}

        self.data["POST"] = {
            key: value
            for key, value in [
                x.split("=") for x in (
                    self.body.split("&") if "&" in self.body else self.body
                )
            ]
        } if self.method.upper() == "POST" else {}

        self.data["COOKIE"] = {
            key: value 
            for key, value in [
                x.split("=") for x in (
                    self.headers["Cookie"].split("; ") if "Cookie" in self.headers else []
                )
            ]
        } if "Cookie" in self.headers else {}
        
    def compile(self) -> str:
        return self.method + " " +  self.path + "?" + "&".join(["=".join([key, value]) for key, value in self.data["GET"].items()]) + " " + self.protocol + "\r\n" + "\r\n".join([key + ": " + value for key, value in self.headers.items()]) + "\r\n\r\n" + self.body