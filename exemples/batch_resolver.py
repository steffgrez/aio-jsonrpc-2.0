import asyncio
import json

from aio_jsonrpc_20 import RequestResolver


async def foo(msg, time):
    await asyncio.sleep(time)
    return 'foobar ' + str(msg)

router = {'foo': foo}
resolver = RequestResolver(router)
json_request = json.dumps([
    {"jsonrpc": "2.0", "method": "foo", "params": ["toto", 1], "id": 1},
    {"jsonrpc": "2.0", "method": "foo", "params": ["tata", 0.5], "id": 2},
    {"jsonrpc": "2.0", "method": "foo", "params": ["tutu", 0.5], "id": 3},
])


async def main():
    json_response = await resolver.handle(json_request)
    print(json_response)

loop = asyncio.get_event_loop()
loop.run_until_complete(main())
