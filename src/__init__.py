from . import Worker
import os, sys

class Server:
    def __init__(self, context):
        if os.name == 'nt':
            print(os.path.abspath(__file__))
            wsl = True if input("Windows still doesn't support fork(), Y/N to use with Windows Subsystem for Linux(WSL)").lower() == "y" else False
            if wsl:
                import __main__
                import subprocess
                if subprocess.run(["wsl", "test", "-f", "/etc/os-release"]).returncode == 0:
                    subprocess.run(["wsl", "python3", os.path.abspath(__file__), "--wsl"])
                else:
                    install = input("WSL not found. Install WSL? Y/N")
                    if install.lower() == "y":
                        # if subprocess.run(["DISM", "/Online", "/Enable-Feature", "/All", "/FeatureName:HypervisorPlatform"]).returncode == 0:
                        subprocess.run(["wsl", "--install", "-d", "Ubuntu"])
                        if subprocess.run(["wsl", "test", "-f", "/etc/os-release"]).returncode == 0:
                            subprocess.run(["wsl", "python3", os.path.abspath(__file__), "--wsl"])
                        else:
                            print("Please Turn On Virtualization In BIOS And Try Again. If The Problem Persists, Please Install WSL Manually.")
                        # else:
                        #     print("Please Run Script As Administrator. Or Run 'DISM /Online /Enable-Feature /All /FeatureName:HypervisorPlatform' In Command Prompt With Administrator Privileges.")

        self.context = context
        self.endpoints = {}
        self.workers = []

    def create_endpoint(self, path):
        def wrapper(handler):
            if(not(self.endpoints.__contains__(path))):
                self.endpoints[path] = handler
                return handler
            else:
                raise AssertionError(f"Endpoint {path}:{handler} Already Exists!")#self.error["urlcatcherexists"])
        return wrapper

    def run(self, sockets):
        for socket_index in range(len(sockets)):
            worker = Worker.Worker(self)
            pid = os.fork()
            if pid == 0:
                while True:
                    request = sockets[socket_index].recv(1024)
                    if not request:
                        break
                    worker.handle(sockets[socket_index], request)
                    sockets[socket_index].close()
            else:
                self.workers.append(pid)
        
    def kill(self):
        for worker in self.workers:
            os.kill(worker, 9)