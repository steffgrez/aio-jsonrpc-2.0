import asyncio
import pytest

from aio_jsonrpc_20.utils import is_valid_params


async def foobar():
    await asyncio.sleep(0.1)


async def foobar1(a, b):
    await asyncio.sleep(0.1)


async def foobar2(a=3, b=4):
    await asyncio.sleep(0.1)


async def foobar3(a, b, c=4):
    await asyncio.sleep(0.1)


@pytest.mark.parametrize('fct, query,expected', [
    # function without args
    (foobar, None, True),
    (foobar, ['a', 'c'], False),
    (foobar, {'a': 1, 'c': 2}, False),
    # function with only args
    (foobar1, None, False),
    (foobar1, ['a'], False),
    (foobar1, ['a', 'c'], True),
    (foobar1, ['a', 'c', 'b'], False),
    (foobar1, {'a': 1}, False),
    (foobar1, {'a': 1, 'b': 2}, True),
    (foobar1, {'a': 1, 'c': 2}, False),
    (foobar1, {'a': 1, 'b': 3, 'c': 2}, False),
    # function with only kwargs
    (foobar2, None, True),
    (foobar2, ['a'], True),
    (foobar2, ['a', 'c'], True),
    (foobar2, ['a', 'c', 'd'], False),
    (foobar2, {'a': 1}, True),
    (foobar2, {'a': 1, 'b': 2}, True),
    (foobar2, {'a': 1, 'c': 2}, False),
    (foobar2, {'a': 1, 'b': 3, 'c': 2}, False),
    # function with mixed args / kwargs
    (foobar3, None, False),
    (foobar3, ['a'], False),
    (foobar3, ['a', 'c'], True),
    (foobar3, ['a', 'c', 'r'], True),
    (foobar3, ['a', 'c', 'r', 's'], False),
    (foobar3, {'a': 1}, False),
    (foobar3, {'a': 1, 'b': 2}, True),
    (foobar3, {'a': 1, 'c': 2}, False),
    (foobar3, {'a': 1, 'd': 2}, False),
    (foobar3, {'a': 1, 'b': 3, 'c': 2}, True),
    (foobar3, {'a': 1, 'b': 3, 'd': 2}, False),
    (foobar3, {'a': 1, 'b': 3, 'c': 2, 'd': 2}, False),

])
def test_is_valid_params(fct, query, expected):
    # function without args
    assert is_valid_params(fct, query) is expected
