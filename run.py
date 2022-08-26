from app import retica
from Retica import Sockets

http_socket = Sockets.HTTP_Socket(Sockets.gethostname(), 80)

if __name__ == "__main__":
    retica.run([http_socket])
