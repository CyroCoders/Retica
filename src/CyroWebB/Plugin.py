class Plugin(object):
    def __init__(self, server, config={}):
        self.server = server
        self.config = config

    def intercept_request(self, request):
        pass

    def intercept_response(self, response):
        pass