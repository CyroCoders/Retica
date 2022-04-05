from .. import Plugin
import socket, threading, select, parse, sys, os, datetime

class Email(Plugin.Plugin):
    def __init__(self, server, config={}):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind(('localhost', 25))
        self.socket.listen(5)
        self.logger = server.logger
        self.workers = []
        self.server = server
        self.config = config
        if "directory" not in config.keys():
            self.config["directory"] = os.path.join("Plugins", "Email")
        self.config["directory"] = os.path.join(os.path.dirname(os.path.abspath(self.server.context)), self.config["directory"])            

    def handle_connection(self, client, address):
        client.send(b'220 The Retica Mail Plugin\r\n')
        client.send(b'250 localhost\r\n')
        while True:
            buffer = ""
            while "\n" not in buffer:
                buffer += client.recv(1024).decode().upper()
            try:
                client_dom = parse.parse('HELO {}',buffer)[0]
                client.send(b'250 OK\r\n')
                break
            except:
                client.send(b'500 Syntax error\r\n')
                
        while True:
            buffer = ""
            while "\n" not in buffer:
                buffer += client.recv(1024).decode().upper()
            try:
                sender = parse.parse('MAIL FROM: <{}>\r\n', buffer)[0]
                client.send(b'250 OK\r\n')
                break
            except:
                client.send(b'500 Syntax error\r\n')
                
        while True:
            buffer = ""
            while "\n" not in buffer:
                buffer += client.recv(1024).decode().upper()
            try:
                recipient = parse.parse('RCPT TO: <{}>\r\n', buffer)[0]
                client.send(b'250 OK\r\n')
                break
            except:
                client.send(b'500 Syntax error\r\n')

        while True:
            buffer = ""
            while "\n" not in buffer:
                buffer += client.recv(1024).decode().upper()
            if buffer == "DATA\r\n":
                client.send(b'354 Start mail input; end with <CRLF>.<CRLF>\r\n')
                break
            else:
                client.send(b'500 Syntax error\r\n')

        while True:
            buffer = ""
            while "\r\n.\r\n" not in buffer:
                buffer += client.recv(1024).decode().upper()
            try:
                client.send(b'250 OK\r\n')
            except:
                client.send(b'500 Syntax error\r\n')
            maildata = buffer.replace("\r\n.\r\n", "").replace("\r\n", "\n")
            break
        
        while True:
            buffer = ""
            while "\n" not in buffer:
                buffer += client.recv(1024).decode().upper()
            if buffer == "QUIT\r\n":
                client.send(b'221 Goodbye\r\n')
                client.close()
                self.save_email(sender, recipient, maildata)
                break
            elif buffer == "RSET\r\n":
                client.send(b'250 OK\r\n')
                self.handle_connection(client, address)
                return
            else:
                client.send(b'500 Syntax error\r\n')

    def save_email(self, sender, recipient, body):
        os.makedirs(os.path.join(self.config["directory"], recipient), exist_ok=True)
        with open(os.path.join(self.config["directory"], recipient, f"{datetime.datetime.now().strftime('%Y-%m-%d-%H%M%S')}.eml"),"w") as f:
            f.write(f"From: {sender}\n")
            f.write(f"To: {recipient}\n")
            f.write(f"Date: {datetime.datetime.now()}\n")
            f.write(f"Subject: \n")
            f.write(f"\n")
            f.write(f"{body}\n")
            
    def run(self):
        try:
            while True:
                read_socks,_,_ = select.select([self.socket], [], [], 0)
                for sock in read_socks:
                    self.workers.append(threading.Thread(target=self.handle_connection, args=(*sock.accept(),)))
                    self.workers[-1].start()
                read_socks = []
        except KeyboardInterrupt:
            self.logger.info("Stopping Mail Server")
            self.socket.close()
            for worker in self.workers:
                worker.join()
            sys.exit(0)
        except Exception as e:
            self.logger.error(f"Error: {e}")
            self.logger.info("Restarting Server")