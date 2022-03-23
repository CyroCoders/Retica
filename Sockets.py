import socket
import ssl

class HTTP_Socket(object):
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def bind(self):
        self.sock.bind((self.host, self.port))
    
    def send(self, data):
        self.sock.send(data)

    def recv(self, size):
        return self.sock.recv(size)

    def close(self):
        self.sock.close()

class HTTPS_Socket(HTTP_Socket):
    def __init__(self, host, port, cert_file, key_file):
        super().__init__(host, port)
        self.ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
        self.ssl_context.load_cert_chain(certfile=cert_file, keyfile=key_file)
        self.sock = self.ssl_context.wrap_socket(self.sock, server_side=True, do_handshake_on_connect=True)

    def bind(self):
        super().bind()
    
    def send(self, data):
        super().send(data)

    def recv(self, size):
        super().recv(size)

    def close(self):
        super().close()