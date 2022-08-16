from . import Worker, Request, Response, Plugin
import os, sys, select
import threading, multiprocessing
import logging

class Server:
    """ The Retica Server

    :param context: The server context to use.
    :type context: str
    :param logger: The logger to use.
    :type logger: logging.Logger
    :param config: The config to use.
    :type config: dict

    :rtype: Server
    """
    def __init__(self, context, logger: logging.Logger=None, config: dict=None):
        """ Initialize the Server.

        :param context: The server context to use.
        :type context: str
        :param logger: The logger to use.
        :type logger: logging.Logger
        :param config: The config to use.
        :type config: dict

        :rtype: Server
        """
        self.logger = logging.getLogger("SERVER") if logger is None else logger
        logging.basicConfig(level=logging.INFO)
        self.config = config
        self.context = context
        self.endpoints = {}
        self.workers = []
        self.plugins = []
        self.runner_plugins = []

    def use_plugin(self, plugin, config):
        """ Use a plugin.
        
        :param plugin: The plugin to use.
        :type plugin: Plugin.Plugin
        :param config: The config to use.
        :type config: dict
        
        :rtype: None"""
        if not issubclass(plugin, Plugin.Plugin):
            raise TypeError("Plugin must be of type Plugin")
        plugin_instance = plugin(self, config)
        self.plugins.append(plugin_instance)
        if hasattr(plugin, "run"):
            self.logger.info(f"Running Plugin {plugin.__name__}")
            self.runner_plugins.append(multiprocessing.Process(target=self.run_plugin, args=(plugin_instance,)).start())

    def run_plugin(self, plugin_instance):
        """ Run a plugin.
        
        :param plugin_instance: The plugin to run.
        :type plugin_instance: Plugin.Plugin
        
        :rtype: None
        """
        if not issubclass(plugin_instance.__class__, Plugin.Plugin):
            raise TypeError("Plugin must be of type Plugin")
        while True:
            plugin_instance.run()

    def create_endpoint(self, path, conditional=None):
        """ A Decorator to create an endpoint.
        
        :param path: The path to use.
        :type path: str
        :param conditional: The conditional to use.
        :type conditional: callable
        
        :rtype: callable"""
        def wrapper(handler):
            if(not(self.endpoints.__contains__(path))):
                self.endpoints[path] = (handler, conditional)
                return handler
            else:
                raise AssertionError(f"Endpoint {path}:{handler} Already Exists!")#self.error["urlcatcherexists"])
        return wrapper

    def run(self, sockets):
        """ Run the server.

        :param sockets: The list of sockets to use.
        :type sockets: list

        :rtype: None
        """
        self.logger.info("Starting Server")
        while True:
            try:
                for socket in sockets:
                    socket.bind(logger=self.logger)
                while True:
                    read_socks,_,_ = select.select(sockets, [], [], 0)
                    for sock in read_socks:
                        self.workers.append(threading.Thread(target=self.handle_request, args=(*sock.sock.accept(),)))
                        self.workers[-1].start()
                    read_socks = []
            except KeyboardInterrupt:
                self.logger.info("Stopping Server")
                for socket in sockets:
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
        worker = Worker.Worker(self)
        if not request:
            return
        worker.handle(socket, request)
        socket.close()