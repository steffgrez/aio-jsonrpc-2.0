#!/usr/bin/env python
import os

from setuptools import setup, find_packages


here = os.path.abspath(os.path.dirname(__file__))
__version__ = None
with open('aio_jsonrpc_20/version.py') as f:
    exec(f.read())

with open(os.path.join(here, 'README.md')) as f:
    README = f.read()
with open(os.path.join(here, 'CHANGES.md')) as f:
    CHANGES = f.read()

desc = "fast JSON-RPC protocol implementation for asyncio, without transport"

setup(
    name="aio-jsonrpc-2.0",
    version=__version__,
    packages=find_packages(),
    # metadata for upload to PyPI
    author="Lahache Stephane",
    author_email='slahache@gmail.com',
    url="https://github.com/steffgrez/aio-jsonrpc-2.0",
    description=desc,
    long_description=README + '\n\n' + CHANGES,
    long_description_content_type='text/markdown',
    keywords='json rpc jsonrpc json-rpc 2.0',

    # Full list:
    # https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Console",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        'Intended Audience :: Developers',
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    license="MIT",
)
