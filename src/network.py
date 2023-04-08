import json
import socket

class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.settimeout(5) 
        self.server = socket.gethostbyname(socket.gethostname())
        self.port = 5555
        self.addr = (self.server, self.port)
        self.id = self.connect()

    def connect(self):
        try:
            self.client.connect(self.addr)
            return json.loads(self.client.recv(20000).decode())
        except Exception as e:
            print("Connection failed:", e)
            pass

    def send(self, data):
        try:
            self.client.send(json.dumps(data).encode())
            reply = self.receive()
            return reply
        except socket.error as e:
            print(e)

    def receive(self):
        data = self.client.recv(20000).decode()
        print("data:", data)
        return json.loads(data)