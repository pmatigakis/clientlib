class ClientlibException(Exception):
    def __init__(self, reason=None, *args):
        super(ClientlibException, self).__init__(reason, *args)

        self.reason = reason


class EndpointError(ClientlibException):
    def __init__(self, reason=None, response=None, *args):
        super(EndpointError, self).__init__(reason, response, *args)

        self.response = response


class ExecutionError(EndpointError):
    pass


class ResponseDeserializationError(EndpointError):
    def __init__(self, reason=None, response=None, errors=None, *args):
        super(ResponseDeserializationError, self).__init__(
            reason, response, errors, *args)

        self.errors = errors
