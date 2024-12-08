import socket

class TelemetryListener:
    def __init__(self, host='0.0.0.0', port=20777):
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind((self.host, self.port))