from aio_jsonrpc_20 import BatchRequestBuilder

batch_builder = BatchRequestBuilder()
id1 = batch_builder.call(method="foo", params={"name": "bar"})
id2 = batch_builder.call(method="foo2", params={"name": "bar"})
print(id1, id2)
batch_builder.notify(method="foo3", params={"name": "bar"})
json_request = batch_builder.get_request()
print(json_request)
