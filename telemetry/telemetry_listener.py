import socket
from telemetry.telemetry_packets import PacketHeader, PacketFactory

class TelemetryListener:
    def __init__(self, host='0.0.0.0', port=20777):
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind((self.host, self.port))

    def receive_packet(self):
        data, _ = self.sock.recvfrom(2048)
        header = PacketHeader(data)
        packet = PacketFactory.create_packet(header, data)
        return packet