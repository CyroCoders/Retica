import parse
from . import Sockets, Request, Response
import os
from typing import Union

class Worker:
    def __init__(self, server):
        self.server = server
    
    def handle(self,socket: Union[Sockets.HTTP_Socket,Sockets.HTTP_Socket],request: Request.request):
        response = Response.response()
        path = request.path
        for plugin in self.server.plugins:
            plugin.intercept_request(request)
        for endpoint, handler in self.server.endpoints.items():
            endpoint = "." + endpoint + "."
            path = "." + path.decode() + "."
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
                arguments = dict(arguments)
                handler(request, response, **arguments)
                for plugin in self.server.plugins:
                    plugin.intercept_response(response)
                socket.sendall(response.compile())