import asyncio
import json
import logging

from aio_jsonrpc_20.exception import (
    InvalidRequestException,
    CustomJsonRpcException
)
from aio_jsonrpc_20.response import ResponseMaker
from aio_jsonrpc_20.utils import (
    is_valid_params,
    check_request,
    lazy_check_request
)


logger = logging.getLogger(__name__)


class RequestResolver(object):
    """This class allow to resolve a request, and build a response."""
    __slots__ = [
        'router',
        'serializer',
        'response_maker',
        'check_request'
    ]

    def __init__(
            self,
            router,
            lazy_check=False,
            error_verbose=True,
            serializer=json
    ):
        self.router = router
        self.response_maker = ResponseMaker(error_verbose)
        self.serializer = serializer

        if lazy_check:
            self.check_request = lazy_check_request
        else:
            self.check_request = check_request

    async def handle(self, str_request):
        # handle encoding
        if isinstance(str_request, bytes):
            str_request = str_request.decode("utf-8")

        # get response from unserialized request
        try:
            request = self.serializer.loads(str_request)
        except (TypeError, ValueError) as decode_error:
            logger.warning('JSON decode error: {}'.format(decode_error))
            response = self.response_maker.get_parse_error(
                data='Could not decode JSON request object.'
            )
        else:
            if request:
                try:
                    # batch request case
                    if isinstance(request, list):
                        coros = []
                        for sub_req in request:
                            coros.append(self._get_response(sub_req))
                        response = await asyncio.gather(*coros)
                        response = [elt for elt in response if elt]
                    # simple request case
                    else:
                        response = await self._get_response(request)
                # handle uncaught exception
                except Exception as e:
                    logger.warning('Unexpected error: ' + str(e))
                    response = self.response_maker.get_internal_error(
                        data=e.args[0]
                    )
            else:
                response = self.response_maker.get_invalid_request(
                    data='Empty request is not allowed'
                )

        # return serialized result
        return self.serializer.dumps(response) if response else ''

    async def _get_response(self, request):
        # get id and check in the same time if request is a dict
        try:
            request_id = request['id']
        except KeyError:
            request_id = None
        except TypeError:
            logger.warning('Request should be a dict object')
            return self.response_maker.get_invalid_request(
                data="Request should be a dict object",
            )

        # check jsonrpc 2.0 specification
        try:
            self.check_request(request)
        except InvalidRequestException as e:
            logger.warning('Invalid request')
            return self.response_maker.get_invalid_request(
                data=e.args[0],
                request_id=request_id
            )

        # get method to call
        try:
            method = self.router[request['method']]
        except KeyError:
            logger.warning('Method not found')
            return self.response_maker.get_method_not_found(
                request_id=request_id
            )
        except TypeError:
            logger.error('Router should be like an dict object')
            return self.response_maker.get_internal_error(
                data="Router should be like an dict object",
            )

        # try to execute method
        try:
            if 'params' in request:
                params = request['params']
                if isinstance(params, dict):
                    result = await method(**params)
                else:
                    result = await method(*params)
            else:
                result = await method()
        except CustomJsonRpcException as e:
            # catch custom error
            logger.warning('CustomError: ' + str(e))
            return self.response_maker.get_server_error(
                code=e.code,
                data=e.data,
                request_id=request_id
            )
        except Exception as e:
            # determine the error's type
            if (
                    isinstance(e, TypeError) and
                    not is_valid_params(method, params)
            ):
                logger.warning('Invalid params')
                return self.response_maker.get_invalid_params(
                    data=e.args[0], request_id=request_id
                )
            else:
                logger.warning('Application error: ' + str(e))
                return self.response_maker.get_internal_error(
                    data=e.args[0], request_id=request_id
                )

        # is notification ?
        if request_id:
            return self.response_maker.get_response(
                result=result, request_id=request_id
            )
        else:
            return None
