import argparse

from .create import create
from .run import run

def main():
    parser = argparse.ArgumentParser(description="The Retica CLI. Retica Is A Performant, Easy To Use Web Server Based On Python With HTTPS & Plugins Support.")
    subparsers = parser.add_subparsers(dest='command')
    
    run_parser = subparsers.add_parser('run', help="Run the current project.")
    run_parser.add_argument("server_object", type=str, const="app:retica", default="app:retica", nargs='?', help="Server object (app:retica)")
    run_parser.add_argument("host", type=str, const="localhost:80", default="localhost:80", nargs='?', help="Hostname and port (localhost:80)")

    subparsers.add_parser('create', help="Create a new project.")

    args = parser.parse_args()
    match args.command:
        case 'create':
            create(args)
            return
        case 'run':
            run(args)
            return
        case None:
            parser.print_help()

if __name__ == "__main__":
    main()