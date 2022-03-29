import parse
from . import Sockets, Request, Response
import os
from typing import Union

class Worker:
    def __init__(self, server):
        self.server = server
    
    def handle(self,socket: Union[Sockets.HTTP_Socket,Sockets.HTTP_Socket],request: Request.request):
        pid = os.fork()
        if pid == 0:
            request.parse()
            response = Response.Response(request)
            path = request.path
            for endpoint,handler in self.server.endpoints:
                endpoint = "." + endpoint + "."
                path = "." + path + "."
                if endpoint[-1] == "/":
                    endpoint = endpoint[:-1]
                if endpoint[1] == "/":
                    endpoint = endpoint[1:]
                if path[-1] == "/":
                    path = path[:-1]
                if path[1] == "/":
                    path = path[1:]
                endpoint = endpoint[1:-1]
                path = path[1:-1]
                if parse.parse(endpoint, path):
                    arguments = parse.parse(endpoint, path)
                    handler(request, response, arguments)
                    break