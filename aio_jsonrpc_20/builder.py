import json

from aio_jsonrpc_20.utils import check_request, lazy_check_request


class RequestBuilder():
    def __init__(self, serializer=json, lazy_check=False):
        self.serializer = serializer
        self.inc = 1

        if lazy_check:
            self.check_request = lazy_check_request
        else:
            self.check_request = check_request

    def call(self, method, params=None):
        request = {
            "jsonrpc": "2.0",
            "method": method,
            "id": self.inc
        }

        if params:
            request["params"] = params

        self.check_request(request)

        self.inc += 1

        if self.serializer:
            return self.serializer.dumps(request)
        else:
            return request

    def notify(self, method, params=None):
        request = {
            "jsonrpc": "2.0",
            "method": method
        }

        if params:
            request["params"] = params

        self.check_request(request)

        if self.serializer:
            return self.serializer.dumps(request)
        else:
            return request


class BatchRequestBuilder():
    BUILDER_CLASS = RequestBuilder

    def __init__(self, serializer=json):
        self.serializer = serializer
        self.builder = self.BUILDER_CLASS(serializer=None)
        self.batch = []

    def call(self, method, params=None):
        request = self.builder.call(method, params)
        self.batch.append(request)

        return request["id"]

    def notify(self, method, params=None):
        request = self.builder.notify(method, params)
        self.batch.append(request)

    def get_request(self):
        if self.serializer:
            return self.serializer.dumps(self.batch)
        else:
            return self.batch

    def purge(self):
        self.batch = []
