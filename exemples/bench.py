import asyncio
from functools import partial
import time

import rapidjson

from aio_jsonrpc_20 import JSONRPCResolver

bulk = 30000
query = '{"jsonrpc": "2.0", "method": "subtract", "params": [42, 23], "id": 1}'


async def bench(func, txt, bulk):
    t0 = time.time()
    for i in range(0, bulk):
        a = await func()
    time_elapsed = time.time() - t0
    print('{0}: {1}s'.format(txt, time_elapsed))
    print('-> {0} op/s'.format(bulk / time_elapsed))

    return a


async def subtract(a, b):
    return a - b


async def main():
    print("#" * 30)
    router = {'subtract': subtract}
    resolver = JSONRPCResolver(router)

    p = partial(resolver.handle, query)
    print(await bench(p, 'aio_jsonrpc_20, json', bulk))

    print("=" * 30)
    resolver = JSONRPCResolver(router, lazy_check=True)

    p = partial(resolver.handle, query)
    print(await bench(p, 'aio_jsonrpc_20, json, lazy check', bulk))

    print("=" * 30)
    resolver = JSONRPCResolver(router, serializer=rapidjson)

    p = partial(resolver.handle, query)
    print(await bench(p, 'aio_jsonrpc_20, rapidjson', bulk))

    print("=" * 30)
    resolver = JSONRPCResolver(router, lazy_check=True, serializer=rapidjson)

    p = partial(resolver.handle, query)
    print(await bench(p, 'aio_jsonrpc_20, rapidjson, lazy_check', bulk))


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
