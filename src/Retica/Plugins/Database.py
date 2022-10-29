import os
from .. import Plugin, Sockets
import json

class RealtimeDatabase(Plugin.Plugin):
    def __init__(self, server, config={"host":"localhost","port":6379}):
        super().__init__(server, config)
        self.database = PersistentDict()
        self.websocket = Sockets.WebSocket(self.config["host"], self.config["port"])

        @self.websocket.create_endpoint("/")
        async def database(websocket):
            data = json.loads(await websocket.recv())
            print(data)
            if data["action"] == "get":
                db = self.database
                for seg in data["loc"].split("/"):
                    try:
                        db = db[seg]
                    except:
                        await websocket.send(json.dumps({"error":"KeyError"}))
                        return
                await websocket.send(json.dumps({"data":db}))
            elif data["action"] == "set":
                data = json.loads(await websocket.recv())
                db = data["value"]
                for seg in reversed(data["loc"].split("/")):
                    db = {seg:db}
                    print(db)
                self.database.update(db)
                await websocket.send(json.dumps({"data":db}))
            elif data["action"] == "exists":
                data = json.loads(await websocket.recv())
                for seg in data["loc"].split("/"):
                    if seg not in self.database:
                        await websocket.send(json.dumps({"data":False}))
                        return
                await websocket.send(json.dumps({"data":True}))
            elif data["action"] == "keys":
                data = json.loads(await websocket.recv())
                db = self.database
                for seg in data["loc"].split("/"):
                    db = db[seg]
                await websocket.send(json.dumps({"data":list(db.keys())}))
            else:
                await websocket.send(json.dumps({"error":"Invalid action"}))
        

    def run(self):
        self.websocket.bind()

class PersistentDict(dict):
    def __init__(self, filename="database.json"):
        super().__init__()
        self.filename = "database.json"
        if os.path.exists(filename):
            with open(filename, "r") as f:
                self.update(json.load(f))
        else:
            self.update({})

    def save(self):
        self._p_changed = False
        with open(self.filename, "w") as f:
            json.dump(self, f)
            print("Saved")

    def __setitem__(self, key, value):
        super().__setitem__(key, value)
        self.save()

    def clear(self):
        super().clear()
        self.save()

    def pop(self, key, default=None):
        super().pop(key, default)
        self.save()

    def popitem(self):
        super().popitem()
        self.save()

    def setdefault(self, key, default=None):
        super().setdefault(key, default)
        self.save()

    def update(self, *args, **kwargs):
        super().update(*args, **kwargs)
        self.save()

    def __del__(self):
        super().__del__()
        self.save()

