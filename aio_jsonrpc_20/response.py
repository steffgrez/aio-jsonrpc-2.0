

class ResponseMaker(object):
    __slot__ = ['error_verbose']

    def __init__(self, error_verbose=True):
        self.error_verbose = error_verbose

    def get_response(self, result, request_id):
        return {
            "jsonrpc": "2.0",
            "result": result,
            "id": request_id
        }

    def get_error(self, code, message, data=None, request_id=None):
        result = {
            "jsonrpc": "2.0",
            "error": {
                "code": code,
                "message": message,
            },
            "id": request_id
        }

        if self.error_verbose and data:
            result["error"]['data'] = data

        return result

    def get_parse_error(self, data=None, request_id=None):
        return self.get_error(
            -32700, 'Parse error', data=data, request_id=request_id
        )

    def get_invalid_request(self, data=None, request_id=None):
        return self.get_error(
            -32600, 'Invalid Request', data=data, request_id=request_id
        )

    def get_method_not_found(self, data=None, request_id=None):
        return self.get_error(
            -32601, 'Method not found', data=data, request_id=request_id
        )

    def get_invalid_params(self, data=None, request_id=None):
        return self.get_error(
            -32602, 'Invalid params', data=data, request_id=request_id
        )

    def get_internal_error(self, data=None, request_id=None):
        return self.get_error(
            -32603, 'Internal error', data=data, request_id=request_id
        )

    def get_server_error(self, code, data, request_id=None):
        return self.get_error(
            code=code,
            message='Server error',
            data=data,
            request_id=request_id
        )
