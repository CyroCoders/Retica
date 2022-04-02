import parse
from . import Sockets, Request, Response
import os, mimetypes
from typing import Union

class Worker:
    """ The Retica Worker

    :param server: The server to use.
    :type server: Server

    :rtype: Worker
    """
    def __init__(self, server):
        """ Initialize the Worker.

        :param server: The server to use.
        :type server: Server

        :rtype: Worker
        """
        self.server = server
    
    def handle(self,socket: Union[Sockets.HTTP_Socket,Sockets.HTTP_Socket],request: Request.request):
        """ Handle a request.

        :param socket: The socket to use.
        :type socket: Sockets.HTTP_Socket
        :param request: The request to handle.
        :type request: Request.request

        :rtype: None
        """
        try:
            response = Response.response()
            path = request.path
            path = path.decode()
            for plugin in self.server.plugins:
                plugin.intercept_request(request)
            for endpoint, (handler,condition) in self.server.endpoints.items():
                proceed = True
                if condition is not None:
                    proceed = condition(request)
                if proceed==True:
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
                        arguments = dict(arguments)
                        handler(request, response, **arguments)
                        for plugin in self.server.plugins:
                            plugin.intercept_response(response)
                        socket.sendall(response.compile())
                        return
                elif isinstance(proceed, Response.response):
                    response.body = proceed
                    socket.sendall(proceed.compile())
                    return
                elif isinstance(proceed, str):
                    response.body = proceed
                    socket.sendall(response.compile())
                    return
                elif isinstance(proceed, bytes):
                    response.body = proceed
                    socket.sendall(proceed.compile())
                    return

            static_path = os.path.join(os.path.dirname(os.path.abspath(self.server.context)), "static",*path.split("/"))
            if os.path.isfile(static_path):
                mimetype = mimetypes.guess_type(static_path)
                response.body = open(static_path, "rb").read()
                response.headers["Content-Type"] = mimetype[0] or "application/octet-stream"
                if mimetype[1]:
                    response.headers["Content-Encoding"] = mimetype[1]
                socket.sendall(response.compile())
                return
            else:
                response.status = "404"
                response.body = "404 Not Found"
                socket.sendall(response.compile())
                return
        except KeyboardInterrupt:
            pass
        except Exception as e:
            self.server.logger.exception(e)