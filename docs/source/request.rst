Retica Request Class
=====================
The Request class is used to build & parse requests.

Creating A Request
^^^^^^^^^^^^^^^^^^^

.. code-block:: python3
   
    import Retica

    request = Retica.Request.request()


Parsing A Request
^^^^^^^^^^^^^^^^^^
An encoded string can be parsed and stored into the request object using the :func:`request.parse()` method.4

.. code-block:: python3
    
    >>> request.parse('GET /?name=Retica HTTP/1.1\r\nHost: www.example.com\r\n\r\npost=1&name=Retica')
    >>> print(type(request))
    <class 'Retica.Request.request'>

Getting Data From The Request
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
The Request class has the following attributes:

1. **method** - The status of the request.
2. **path** - The body of the request.
3. **protocol** - The protocol of the request.
4. **headers** - The headers of the request.
5. **data** - The data of the request (Changing this variable doesn't modify the compiled response).

.. code-block:: python3
    
    >>> print(request.method)
    GET
    >>> print(request.path)
    /
    >>> print(request.protocol)
    HTTP/1.1
    >>> print(request.headers)
    {'Host': 'www.example.com'}
    >>> print(request.data['GET'])
    {'name': 'Retica'}
    >>> print(request.data['POST'])
    {'post': '1', 'name': 'Retica'}
    >>> print(request.data['COOKIE'])
    {}


Compiling The Request Into A String
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
The request can be compiled using the :func:`request.compile()` method.

.. code-block:: python3
    
    >>> request.compile()
    'GET /?name=Retica HTTP/1.1\r\nHost: www.example.com\r\n\r\npost=1&name=Retica'