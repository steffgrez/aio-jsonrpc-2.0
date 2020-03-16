# aio-jsonrpc-2.0

[![Build Status](https://travis-ci.org/steffgrez/aio-jsonrpc-2.0.svg?branch=master)](https://travis-ci.org/steffgrez/aio-jsonrpc-2.0)
[![Coverage Status](https://coveralls.io/repos/github/steffgrez/aio-jsonrpc-2.0/badge.svg?branch=master)](https://coveralls.io/github/steffgrez/aio-jsonrpc-2.0?branch=master)

## Description
json rpc 2.0 protocol implementation for asyncio, without transport.

specification: http://www.jsonrpc.org/

## Usage:
Example to resolve request:


```python
import asyncio
import json

from aio_jsonrpc_20 import RequestResolver


async def foo(msg):
    await asyncio.sleep(0.1)
    return 'foobar ' + str(msg)

router = {'foo': foo}
resolver = RequestResolver(router)
json_request = json.dumps(
    {"jsonrpc": "2.0", "method": "foo", "params": ["toto"], "id": 1}
)


async def main():
    json_response = await resolver.handle(json_request)
    print(json_response)

loop = asyncio.get_event_loop()
loop.run_until_complete(main())
```
Result:
```JSON
{"jsonrpc": "2.0", "result": "foobar toto", "id": 1}
```

Example to build request:
```python
from aio_jsonrpc_20 import RequestBuilder

builder = RequestBuilder()
json_request = builder.call(method="foo", params={"name": "bar"})
print(json_request)
json_request = builder.call(method="foo", params={"name": "bar2"})
print(json_request)
json_request = builder.notify(method="log", params=["hello"])
print(json_request)
```

Result:
```JSON
{"jsonrpc": "2.0", "method": "foo", "params": {"name": "bar"}, "id": 1}
{"jsonrpc": "2.0", "method": "foo", "params": {"name": "bar2"}, "id": 2}
{"jsonrpc": "2.0", "method": "log", "params": ["hello"]}

```

Example to build batch request:
```python
from aio_jsonrpc_20 import BatchRequestBuilder

batch_builder = BatchRequestBuilder()
id1 = batch_builder.call(method="foo", params={"name": "bar"})
id2 = batch_builder.call(method="foo2", params={"name": "bar"})
print(id1, id2)
batch_builder.notify(method="foo3", params={"name": "bar"})
json_request = batch_builder.get_request()
print(json_request)
```

Result:
```JSON
1 2
[
    {"jsonrpc": "2.0", "method": "foo", "params": {"name": "bar"}, "id": 1},
    {"jsonrpc": "2.0", "method": "foo2", "params": {"name": "bar"}, "id": 2},
    {"jsonrpc": "2.0", "method": "foo3", "params": {"name": "bar"}}
]
```

## TODO:
* Fix definitely interface for builders
* More Test
* Documentation
* Optimisation
* ...

## Testing:
py.test --cov=aio_jsonrpc_20 --cov-report term-missing tests/