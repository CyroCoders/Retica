def run(args):
    import os.path
    import sys
    import importlib

    from Retica import Sockets

    sys.path.insert(0,os.getcwd())
    f,a = args.server_object.split(":")
    m = importlib.import_module(f)

    server = getattr(m, a)

    if __name__ == "Retica.cli.run":
        sock = Sockets.HTTP_Socket(args.host.split(":")[0], int(args.host.split(":")[1]))
        server.run([sock])