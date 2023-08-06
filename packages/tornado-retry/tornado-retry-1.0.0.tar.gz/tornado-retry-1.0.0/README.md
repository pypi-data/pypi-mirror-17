Tornado Retry
=============

I have been looking for a robust, Tornado friendly retry utility but nothing
generic came up. So I decided to make one.

Usage:
------

```python
from functools import partial
from tornado import gen, httpclient
from tornado_retry import retry

@gen.coroutine
def get_server_data(url):
    http_client = httpclient.AsyncHTTPClient()

    response = yield retry(partial(http_client.fetch, url))

    raise gen.Return(response)
```

Conditional loops
-----------------

Useful when you need to decide if continuing the loop is a good idea.

```python
def connect_to_server(addr, port):
    pass # imagine we connected to a real server here, but it could fail ..

def check_errors(exc_info):
    if isinstance(exc_info[1], (ValueError, TypeError)):
        # these types of errors are never going to succeed
        return False

    # otherwise retry all other exceptions


@gen.coroutine
def get_data():
    yield retry(connect_to_server, on_error=check_errors)
```

Testing
-------

```sh
$ pip install -r requirements_dev.txt
$ nosetests
```
