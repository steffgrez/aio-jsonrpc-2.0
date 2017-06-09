import inspect

from aio_jsonrpc_20.exception import InvalidRequestException


JSONRPC_VERSION = "2.0"
REQUIRED_FIELDS = set(["jsonrpc", "method"])
POSSIBLE_FIELDS = set(["jsonrpc", "method", "params", "id"])


def lazy_check_request(request):
    pass


def check_request(request):
    # check request's keys
    request_keys = set(request.keys())
    extra = request_keys - POSSIBLE_FIELDS
    missed = REQUIRED_FIELDS - request_keys
    if len(extra) > 0 or len(missed) > 0:
        msg = (
            "Invalid request."
            " Extra fields: {0},"
            " Missed fields: {1}"
        )
        raise InvalidRequestException(msg.format(extra, missed))

    # check jsonrpc's version
    if request['jsonrpc'] != JSONRPC_VERSION:
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


def is_valid_params(func, params):
    # inspect method
    spec = inspect.getfullargspec(func)
    if spec.defaults:
        required = spec.args[:-len(spec.defaults)]
    else:
        required = spec.args

    # checks params validity
    if not params:
        if required:
            return False
    elif isinstance(params, list):
        if len(params) < len(required) or len(params) > len(spec.args):
            return False
    else:
        params_keys = set(params.keys())
        if (
                len(params_keys) > len(spec.args) or
                len(set(params_keys) & set(required)) != len(required) or
                len(set(params_keys) - set(spec.args)) > 0
        ):
            return False

    return True
