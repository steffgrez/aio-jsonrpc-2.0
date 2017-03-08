# aio-jsonrpc-2.0

-- **Still in beta** --

## Description
json rpc 2.0 protocol implementation for asyncio, without transport.

specification: http://www.jsonrpc.org/

## Usage:
Simple example:
```python
from aio_jsonrpc_20 import JSONRPCResolver

def foo(msg)
    return 'foobar ' + str(msg)

router = {'foo': foo}
resolver = JSONRPCResolver(router)

json_request = {"jsonrpc": "2.0", "method": "foo", "params": ["toto"], "id": 1}
json_response = resolver.handle(json_request)

print json_response
```
Result:
```
{"jsonrpc": "2.0", "result": "foobar toto", "id": 1}
```

## TODO:
* Fix definitely interface
* More Test
* Documentation
* Optimisation
* ...

## Testing:
py.test --cov=aio_jsonrpc_20 --cov-report term-missing tests/