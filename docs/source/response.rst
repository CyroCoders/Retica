Retica Response Class
=====================
The Response class is used to build & parse responses.

Creating A Response
^^^^^^^^^^^^^^^^^^^

.. code-block:: python3
   
    import Retica

    response = Retica.Response.response()

Modifying The Response
^^^^^^^^^^^^^^^^^^^^^^
The Response class has the following attributes:

1. **status** - The status of the response.
2. **headers** - The headers of the response.
3. **body** - The body of the response.
4. **protocol** - The protocol of the response.
5. **content_type** - The content type of the response.
6. **connection** - The connection status after the response has been received.

.. code-block:: python3
    
    response.status = 200
    response.headers = {'set-cookie': 'session=123456789'}
    response.body = '<h1>Hello World!</h1>'
    response.protocol = 'HTTP/1.1'
    response.content_type = 'text/html'
    response.connection = 'keep-alive'

Parsing A Response
^^^^^^^^^^^^^^^^^^
An encoded string can be parsed and stored into the response object using the :func:`response.parse()` method.4

.. code-block:: python3
    
    >>> response.parse('HTTP/1.1 200 OK\r\nContent-Type: text/html\r\nConnection: keep-alive\r\nSet-Cookie: session=123456789\r\n\r\n<h1>Hello World!</h1>')
    >>> print(type(response))

Compiling The Response Into A String
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
The response can be compiled using the :func:`response.compile()` method.

.. code-block:: python3
    
    >>> response.compile()
    'HTTP/1.1 200 OK\r\nContent-Type: text/html\r\nConnection: keep-alive\r\nSet-Cookie: session=123456789\r\n\r\n<h1>Hello World!</h1>'