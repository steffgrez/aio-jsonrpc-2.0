

class ResponseHandler(object):

    __slot__ = ['error_verbose']

    JSONRPC_VERSION = "2.0"

    def __init__(self, error_verbose=True):
        self.error_verbose = error_verbose

    def get_response(self, result, request_id):
        return {
            "jsonrpc": "2.0",
            "result": result,
            "id": request_id
        }

    def get_error_response(self, code, message, data=None, request_id=None):
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

    def get_parse_error_response(self, data=None, request_id=None):
        return self.get_error_response(
            -32700, 'Parse error', data=data, request_id=request_id
        )

    def get_invalid_request_response(self, data=None, request_id=None):
        return self.get_error_response(
            -32600, 'Invalid Request', data=data, request_id=request_id
        )

    def get_method_not_foud_response(self, data=None, request_id=None):
        return self.get_error_response(
            -32601, 'Method not found', data=data, request_id=request_id
        )

    def get_invalid_params_response(self, data=None, request_id=None):
        return self.get_error_response(
            -32602, 'Invalid params', data=data, request_id=request_id
        )

    def get_internal_error_response(self, data=None, request_id=None):
        return self.get_error_response(
            -32603, 'Internal error', data=data, request_id=request_id
        )

    def get_server_error_response(self, data=None, request_id=None):
        return self.get_error_response(
            -32000, 'Server error', data=data, request_id=request_id
        )
