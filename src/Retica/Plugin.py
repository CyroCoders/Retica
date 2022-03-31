class Plugin(object):
    """ Base Plugin Class

    :param server: The server to use.
    :type server: Server
    :param config: The config to use.
    :type config: dict

    :rtype: Plugin
    """
    def __init__(self, server, config={}):
        """ Initialize the Plugin.
        
        :param server: The server to use.
        :type server: Server
        :param config: The config to use.
        :type config: dict
        
        :rtype: Plugin
        """
        self.server = server
        self.config = config

    def intercept_request(self, request):
        """ Intercept a request.
        
        :param request: The request to intercept.
        :type request: Request
        
        :rtype: Request
        """
        pass

    def intercept_response(self, response):
        """ Intercept a response.

        :param response: The response to intercept.
        :type response: Response

        :rtype: Response
        """
        pass