from aio_jsonrpc_20.utils import is_valid_params


class RequestHandler(object):

    __slots__ = ['response_handler', 'router', 'lazy_check']

    JSONRPC_VERSION = "2.0"
    REQUIRED_FIELDS = set(["jsonrpc", "method"])
    POSSIBLE_FIELDS = set(["jsonrpc", "method", "params", "id"])

    def __init__(self, response_handler, router, lazy_check=False):
        self.lazy_check = lazy_check
        self.response_handler = response_handler
        self.router = router

    async def get_response(self, request):
        # batch request case
        if isinstance(request, list):
            response_batch = []
            for sub_request in request:
                response = await self._get_response(sub_request)
                if response:
                    response_batch.append(response)
            return response_batch
        # simple request case
        else:
            return await self._get_response(request)

    async def _get_response(self, request):
        # check the request structure
        if not isinstance(request, dict):
            return self.response_handler.get_invalid_request_response(
                data="Request should be an object (dict)",
            )
        request_id = request['id'] if 'id' in request else None

        # check request and determine method to execute
        if not self.lazy_check:
            try:
                self.check_request(request)
            except InvalidRequestException as e:
                return self.response_handler.get_invalid_request_response(
                    data=e.args[0],
                    request_id=request_id
                )

        # get method
        try:
            method = self.router[request['method']]
        except KeyError:
            return self.response_handler.get_method_not_foud_response(
                request_id=request_id
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

        except Exception as e:
            # determine type of error
            if (
                    isinstance(e, TypeError) and
                    not is_valid_params(method, params)
            ):
                return self.response_handler.get_invalid_params_response(
                    data=e.args[0], request_id=request_id
                )
            else:
                return self.response_handler.get_internal_error_response(
                    data=e.args[0], request_id=request_id
                )

        # is notification ?
        if request_id:
            return self.response_handler.get_response(
                result=result, request_id=request_id
            )
        else:
            return ''

    def check_request(self, request):
        # check request's keys
        request_keys = set(request.keys())
        extra = request_keys - self.POSSIBLE_FIELDS
        missed = self.REQUIRED_FIELDS - request_keys
        if len(extra) > 0 or len(missed) > 0:
            msg = (
                "Invalid request."
                " Extra fields: {0},"
                " Missed fields: {1}"
            )
            raise InvalidRequestException(msg.format(extra, missed))

        # check jsonrpc's version
        if request['jsonrpc'] != self.JSONRPC_VERSION:
            raise InvalidRequestException(
                'version of the JSON-RPC protocol '
                'MUST be exactly "2.0"'
            )

        # check method
        method = request['method']
        if not isinstance(method, str):
            raise InvalidRequestException("Method should be string")

        if method.startswith("rpc."):
            raise InvalidRequestException(
                "Method names that begin with the word rpc followed "
                "by a period character (U+002E or ASCII 46) are "
                "reserved for rpc-internal methods and extensions "
                "and MUST NOT be used for anything else."
            )

        # check params
        if 'params' in request:
            params = request['params']
            params_check = isinstance(params, (list, tuple, dict))
            if params and not params_check:
                raise InvalidRequestException(
                    "Incorrect params: {0}".format(params)
                )

        # check id
        if 'id' in request:
            request_id = request['id']
            if request_id and not isinstance(request_id, (str, int)):
                raise InvalidRequestException(
                    "Incorrect id: {0}".format(request_id)
                )


class InvalidRequestException(Exception):
    pass
