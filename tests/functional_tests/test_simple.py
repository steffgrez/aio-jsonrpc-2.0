import asyncio
import pprint

import json
import pytest

from aio_jsonrpc_20 import (
    RequestResolver,
    CustomJsonRpcException
)


async def subtract(minuend, subtrahend):
    await asyncio.sleep(0.1)
    return minuend - subtrahend


async def raise_error():
    await asyncio.sleep(0.1)
    raise Exception('error')


async def raise_custom_error():
    await asyncio.sleep(0.1)
    raise CustomJsonRpcException(-32004, 'error')


async def update(a, b, c, d, e):
    await asyncio.sleep(0.1)


async def foobar(msg):
    await asyncio.sleep(0.1)
    return 'foobar ' + str(msg)


async def notify():
    await asyncio.sleep(0.1)


router = {
    'subtract': subtract,
    'update': update,
    'foobar': foobar,
    'raise_error': raise_error,
    'raise_custom_error': raise_custom_error,
    'notify': notify,
}

resolver = RequestResolver(router, error_verbose=False)


@pytest.mark.asyncio
@pytest.mark.parametrize('query,expected', [
    (
        """{"jsonrpc": "2.0", "method": "subtract", "params": [42, 23], "id": 1}""",  # NOQA
        """{"jsonrpc": "2.0", "result": 19, "id": 1}"""
    ),
    (
        """{"jsonrpc": "2.0", "method": "foobar", "params": ["toto"], "id": 1}""",  # NOQA
        """{"jsonrpc": "2.0", "result": "foobar toto", "id": 1}"""
    ),
    (
        """{"jsonrpc": "2.0", "method": "foobar", "params": ["toté パイソン"], "id": 1}""",  # NOQA
        """{"jsonrpc": "2.0", "result": "foobar toté パイソン", "id": 1}"""
    ),
    (
        """{"jsonrpc": "2.0", "method": "subtract", "params": [23, 42], "id": 2}""",  # NOQA
        """{"jsonrpc": "2.0", "result": -19, "id": 2}"""
    ),
    (
        """{"jsonrpc": "2.0", "method": "subtract", "params": {"subtrahend": 23, "minuend": 42}, "id": 3}""",  # NOQA
        """{"jsonrpc": "2.0", "result": 19, "id": 3}"""
    ),
    (
        """{"jsonrpc": "2.0", "method": "subtract", "params": {"minuend": 42, "subtrahend": 23}, "id": 4}""",  # NOQA
        """{"jsonrpc": "2.0", "result": 19, "id": 4}"""
    ),
    (
        """{"jsonrpc": "2.0", "method": "update", "params": [1, 2, 3, 4, 5]}""",  # NOQA
        ''
    ),
    (
        """{"jsonrpc": "2.0", "method": "notify"}""",
        ''
    ),
    (
        """{"jsonrpc": "2.0", "method": "foobar2", "id": "1"}""",
        """{"jsonrpc": "2.0", "error": {"code": -32601, "message": "Method not found"}, "id": "1"}"""  # NOQA
    ),
    (
        """{"jsonrpc": "2.0", "method": "foobar, "params": "bar", "baz"]""",
        """{"jsonrpc": "2.0", "error": {"code": -32700, "message": "Parse error"}, "id": null}"""  # NOQA
    ),
    (
        """{"jsonrpc": "2.0", "method": 1, "params": "bar"}""",
        """{"jsonrpc": "2.0", "error": {"code": -32600, "message": "Invalid Request"}, "id": null}"""  # NOQA
    ),
    (
        """{"jsonrpc": "2.0", "method": "subtract", "params": [23], "id": 1}""",  # NOQA
        """{"jsonrpc": "2.0", "error": {"code": -32602, "message": "Invalid params"}, "id": 1}"""  # NOQA
    ),
    (
        """{"jsonrpc": "2.0", "method": "raise_error", "id": 1}""",  # NOQA
        """{"jsonrpc": "2.0", "error": {"code": -32603, "message": "Internal error"}, "id": 1}"""  # NOQA
    ),
    (
        """{"jsonrpc": "2.0", "method": "raise_custom_error", "id": 1}""",  # NOQA
        """{"jsonrpc": "2.0", "error": {"code": -32004, "message": "Server error"}, "id": 1}"""  # NOQA
    ),
    (
        """{"jsonrpc": "2.0", "method": "foobar", "params": "toto", "id": 1}""",  # NOQA
        """{"jsonrpc": "2.0", "error": {"code": -32600, "message": "Invalid Request"}, "id": 1}"""  # NOQA
    ),
])
async def test_init(query, expected):
    decoded_expected = json.loads(expected) if expected else expected
    result = await resolver.handle(query)
    decoded_result = json.loads(result) if result else result

    assert decoded_expected == decoded_result
