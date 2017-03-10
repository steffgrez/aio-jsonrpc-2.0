class AioJsonRpcException(Exception):
    pass


class InvalidRequestException(AioJsonRpcException):
    pass
