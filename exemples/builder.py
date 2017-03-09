from aio_jsonrpc_20 import RequestBuilder

builder = RequestBuilder()
json_request = builder.call(method="foo", params={"name": "bar"})
print(json_request)
json_request = builder.call(method="foo", params={"name": "bar2"})
print(json_request)
json_request = builder.notify(method="log", params=["hello"])
print(json_request)
