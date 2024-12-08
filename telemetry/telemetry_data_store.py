from telemetry.telemetry_packets import CarTelemetryPacket, CarStatusPacket, LapDataPacket, CarDamageDataPacket

class TelemetryDataStore:
    def __init__(self):
        self.telemetry_packets = []
        self.status_packets = []
        self.lap_data_packets = []
        self.car_damage_packets = []

    def add_packet(self, packet):
        if isinstance(packet, CarTelemetryPacket):
            self.telemetry_packets.append(packet)
        elif isinstance(packet, CarStatusPacket):
            self.status_packets.append(packet)
        elif isinstance(packet, LapDataPacket):
            self.lap_data_packets.append(packet)
        elif isinstance(packet, CarDamageDataPacket):
            self.car_damage_packets.append(packet)