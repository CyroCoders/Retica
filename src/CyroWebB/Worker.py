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
        for endpoint, (handler,condition) in self.server.endpoints.items():
            proceed = True
            if condition is not None:
                proceed = condition(request)
            if proceed==True:
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
            elif isinstance(proceed, Response.response):
                response.body = proceed
                socket.sendall(proceed.compile())
            elif isinstance(proceed, str):
                response.body = proceed
                socket.sendall(response.compile())
            elif isinstance(proceed, bytes):
                response.body = proceed
                socket.sendall(proceed.compile())