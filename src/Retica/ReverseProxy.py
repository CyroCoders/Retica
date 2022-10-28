import logging, threading, select, sys
from .Worker import Worker
from . import Sockets, Request
from typing import Union

class ReverseProxy(object):
    def __init__(self, sockets, logger=None, config=None):
        self.logger = logging.getLogger("SERVER") if logger is None else logger
        logging.basicConfig(level=logging.INFO)
        self.sockets = sockets
        self.config = config
        self.endpoints = {}
        self.workers = []
        self.plugins = []
        self.runner_plugins = []

    def run(self):
        while True:
            try:
                for socket in self.sockets:
                    socket.bind(logger=self.logger)
                while True:
                    read_socks,_,_ = select.select(self.sockets, [], [], 0)
                    for sock in read_socks:
                        self.workers.append(threading.Thread(target=self.handle_request, args=(*sock.sock.accept(),)))
                        self.workers[-1].start()
                    read_socks = []
            except KeyboardInterrupt:
                self.logger.info("Stopping Server")
                for socket in self.sockets:
                    socket.close()
                for worker in self.workers:
                    worker.join()
                sys.exit(0)
            except Exception as e:
                self.logger.error(f"Error: {e}")
                self.logger.info("Restarting Server")

    def handle_request(self, socket, address):
        """ Handle a request.

        :param socket: The socket to use.
        :type socket: socket.socket
        :param address: The address to use.
        :type address: tuple
        
        :rtype: None
        """
        request = Request.request()
        request.parse(socket.recv(1024))
        self.logger.info(f"New Connection From {address} For {request.path.decode()}")
        for server in self.config:
            for condition in server["conditional"]:
                if condition(request) == False:
                    continue
            worker = Worker(self)
            if not request:
                return
            worker.handle(socket, request)
            socket.close()
            return

        worker = Worker(self.config["default"])
        if not request:
            return
        worker.handle(socket, request)
        socket.close()
        