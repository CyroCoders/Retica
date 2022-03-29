from . import Worker, Request, Response
import os, sys, select
import threading
import logging

class Server:
    def __init__(self, context, config=None):
        self.config = config
        self.context = context
        self.endpoints = {}
        self.workers = []

    def create_endpoint(self, path):
        def wrapper(handler):
            if(not(self.endpoints.__contains__(path))):
                self.endpoints[path] = handler
                return handler
            else:
                raise AssertionError(f"Endpoint {path}:{handler} Already Exists!")#self.error["urlcatcherexists"])
        return wrapper

    def run(self, sockets):
        for socket in sockets:
            socket.bind()
        while True:
            read_socks,_,_ = select.select(sockets, [], [])
            for sock in read_socks:
                self.workers.append(threading.Thread(target=self.handle_request, args=(*sock.sock.accept(),)))
                self.workers[-1].start()
            read_socks = []

    def handle_request(self, socket, address):
        logging.info(f"New Connection From {address}")
        request = Request.request()
        request.parse(socket.recv(1024))
        worker = Worker.Worker(self)
        if not request:
            return
        worker.handle(socket, request)
        socket.close()

    def kill(self):
        for worker in self.workers:
            os.kill(worker, 9)