import asyncio
import socket
import ssl
import websockets

def gethostname():
    """ Get the hostname of the current machine. """
    return socket.gethostname()

class HTTP_Socket(object):
    """ A HTTP Socket

    :param host: The host to bind to.
    :type host: str
    :param port: The port to bind to.
    :type port: int

    :rtype: HTTP_Socket
    """
    def __init__(self, host, port):
        """ Initialize the HTTP Socket.
        
        :param host: The host to bind to.
        :type host: str
        :param port: The port to bind to.
        :type port: int

        :rtype: HTTP_Socket
        """
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def bind(self,logger=None):
        """ Bind the socket to the host and port.

        :param logger: The logger to use.
        :type logger: Logger

        :rtype: None
        """
        self.sock.bind((self.host, self.port))
        self.sock.listen(5)
        if logger:
            logger.info(f"Listening On {self.host}:{self.port}")
    
    def send(self, data):
        """ Send data to the socket.

        :param data: The data to send.
        :type data: bytes

        :rtype: None
        """
        self.sock.send(data)

    def recv(self, size):
        """ Receive data from the socket.

        :param size: The size of the data to receive.
        :type size: int

        :rtype: bytes
        """
        return self.sock.recv(size)

    def close(self):
        """ Close the socket.
    
        :rtype: None
        """
        self.sock.close()

    def fileno(self):
        """ Get the file descriptor of the socket.

        :rtype: int
        """
        return self.sock.fileno()
        return self.sock.fileno()

class HTTPS_Socket(HTTP_Socket):
    """ A HTTPS Socket
    
    :param host: The host to bind to.
    :type host: str
    :param port: The port to bind to.
    :type port: int
    :param cert_file: The certificate file to use.
    :type cert_file: str
    :param key_file: The key file to use.
    :type key_file: str

    :rtype: HTTPS_Socket
    """
    def __init__(self, host, port, cert_file, key_file):
        """ Initialize the HTTPS Socket.
        
        :param host: The host to bind to.
        :type host: str
        :param port: The port to bind to.
        :type port: int
        :param cert_file: The certificate file to use.
        :type cert_file: str
        :param key_file: The key file to use.
        :type key_file: str
        
        :rtype: HTTPS_Socket"""
        super().__init__(host, port)
        self.ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
        self.ssl_context.load_cert_chain(certfile=cert_file, keyfile=key_file)
        self.sock = self.ssl_context.wrap_socket(self.sock, server_side=True, do_handshake_on_connect=True)

    def bind(self):
        """ Bind the socket to the host and port.

        :param logger: The logger to use.
        :type logger: Logger

        :rtype: None
        """
        super().bind()
    
    def send(self, data):
        """ Send data to the socket.
        
        :param data: The data to send.
        :type data: bytes
        
        :rtype: None
        """
        super().send(data)

    def recv(self, size):
        """ Receive data from the socket.

        :param size: The size of the data to receive.
        :type size: int
        
        :rtype: bytes
        """
        super().recv(size)

    def close(self):
        """ Close the socket.

        :rtype: None
        """
        super().close()

class WebSocket(object):
    """ A WebSocket

    :param host: The host to bind to.
    :type host: str
    :param port: The port to bind to.
    :type port: int

    :rtype: WebSocket
    """
    def __init__(self, host, port):
        """ Initialize the WebSocket.

        :param host: The host to bind to.
        :type host: str
        :param port: The port to bind to.
        :type port: int

        :rtype: WebSocket
        """
        self.host = host
        self.port = port
        self.sock = websockets.serve(self.handle, host, port)
        self.endpoints = {}

    def create_endpoint(self, path, conditional=None):
        """ Create an endpoint for the WebSocket.

        :param path: The path to the endpoint.
        :type path: str

        :rtype: None
        """
        def wrapper(handler):
            if(not(self.endpoints.__contains__(path))):
                self.endpoints[path] = (handler, conditional)
                return handler
            else:
                raise AssertionError(f"Endpoint {path}:{handler} Already Exists!")#self.error["urlcatcherexists"])
        return wrapper

    async def handle(self, websocket, path):
        """ Handle the WebSocket.

        :param websocket: The WebSocket to handle.
        :type websocket: websockets.WebSocketServerProtocol
        :param path: The path to the endpoint.
        :type path: str

        :rtype: None
        """
        if(self.endpoints.__contains__(path)):
            handler, conditional = self.endpoints[path]
            if(conditional):
                if(conditional(websocket)):
                    await handler(websocket)
            else:
                await handler(websocket)
        else:
            raise AssertionError(f"Endpoint {path} Does Not Exist!")

    def bind(self, logger=None):
        """ Bind the socket to the host and port.

        :param logger: The logger to use.
        :type logger: Logger

        :rtype: None
        """
        asyncio.get_event_loop().run_until_complete(self.sock)
        asyncio.get_event_loop().run_forever()
        if logger:
            logger.info(f"Listening On {self.host}:{self.port}")