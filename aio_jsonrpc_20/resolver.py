"""
from fast_jsonrpc import JSONRPCResolver

def foo(msg)
    return 'foobar ' + str(msg)

router = {'foo': foo}
resolver = JSONRPCResolver(router)

json_request = {"jsonrpc": "2.0", "method": "foo", "params": ["toto"], "id": 1}
json_response = resolver.handle(json_request)

print json_response
-> {"jsonrpc": "2.0", "result": "foobar toto", "id": 1}
"""


import json

from aio_jsonrpc_20.handler.request import RequestHandler
from aio_jsonrpc_20.handler.response import ResponseHandler


class JSONRPCResolver(object):

    __slots__ = [
        'serializer',
        'response_handler',
        'request_handler'
    ]

    def __init__(
            self,
            router,
            lazy_check=False,
            error_verbose=True,
            serializer=json
    ):
        self.serializer = serializer

        self.response_handler = ResponseHandler(error_verbose)
        self.request_handler = RequestHandler(
            self.response_handler, router, lazy_check
        )

    async def handle(self, str_request):
        response = None
        try:
            # handle encoding
            if isinstance(str_request, bytes):
                str_request = str_request.decode("utf-8")

            # get response from unserialized request
            try:
                request = self.serializer.loads(str_request)
            except (TypeError, ValueError):
                response = self.response_handler.get_parse_error_response(
                    data='Bad formatted json'
                )
            else:
                if not request:
                    response = self.response_handler \
                        .get_invalid_request_response(
                            data='Empty request is not allowed'
                        )
                else:
                    response = await self.request_handler.get_response(request)

        except Exception as e:
            # handle unexpected exception
            response = self.response_handler.get_internal_error_response(
                data=e.args[0]
            )

        # return serialized result
        return self.serializer.dumps(response) if response else ''


class JSONRPCException(Exception):
    pass
