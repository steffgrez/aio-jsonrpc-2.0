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
