import logging


logger = logging.getLogger(__name__)


class AioJsonRpcException(Exception):
    pass


class InvalidRequestException(AioJsonRpcException):
    pass


class CustomJsonRpcException(AioJsonRpcException):
    def __init__(self, code, data):
        self.code = code
        self.data = data

        if not (-32099 <= code <= -32000):
            logger.error(
                "Wrong Custom Error, custom error must be "
                "between -32099 and -32000"
            )
