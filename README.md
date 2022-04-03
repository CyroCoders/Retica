![Retica Banner](https://github.com/CyroCoders/Retica/raw/media/Retica-Banner.png)

[![Documentation Status](https://readthedocs.org/projects/retica/badge/?version=latest)](https://retica.readthedocs.io/en/latest/?badge=latest)

# The Retica Backend Server

Retica Is A Performant, Easy To Use Web Server Based On Python With HTTPS & Plugins Support.

## Retica V/S Flask

The Following Graph Shows A Performane Comparision Between Flask & Retica.

1. Total 5,000 Requests with 5 Concurrent Connections
2. Total 20,000 Requests with 20 Concurrent Connections

![Flask V/S Retica](https://github.com/CyroCoders/Retica/raw/media/Flask-VS-Retica.png)

## Installing Retica

The easiest way to install Retica is to use the pip command line tool.

``` shell
$~ pip install retica
```

## Creating A Retica Server

Once you have installed Retica, you can import it into your Python
environment. The server class is used to create a server, in which you
can add endpoints(locations) and open HTTP(s) ports.

``` python
import Retica
retica = Retica.Server(__name__)
```

## Creating An Endpoint

Endpoints are functions that are assigned to a location and are called
when a request is made to that location.

``` python
@retica.create_endpoint("/hello/{name}")
def index(request: Retica.Request.request, response: Retica.Response.response, **data):
    response.body = f"Hello {data['name']}"
```

## Creating A Socket

Sockets are used to open a server port that listens for incoming
connections. The server will listen on the specified port and host.
Sockets can use 2 protocols:

1. HTTP
2. HTTPS (Certificate & key files are required)

- You can also create your own protocols(In Development).

``` python
http_socket = Retica.Sockets.HTTP_Socket("localhost", 80)
https_socket = Retica.Sockets.HTTPS_Socket("localhost", 443, "cert.pem", "key.pem")
```

## Running the Server

To run the server, you must call the run method on the server. An array
of sockets should be passed in as an argument.

``` python
if __name__ == "__main__":
    server.run([
        http_socket,
        https_socket
    ])
```

## Boilerplate

This is the boilerplate code that you will need to create your own
server.

``` python
import Retica
retica = Retica.Server(__name__)

@retica.create_endpoint("/hello/{name}")
def index(request: Retica.Request.request, response: Retica.Response.response, **data):
    response.body = f"Hello {data['name']}"

http_socket = Retica.Sockets.HTTP_Socket(Retica.Sockets.gethostname(), 80)

if __name__ == "__main__":
    server.run([http_socket])
```
