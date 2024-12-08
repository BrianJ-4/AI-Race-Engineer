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

    def get_latest_telemetry(self):
        if self.telemetry_packets:
            return self.telemetry_packets[-1]
        else:
            return None

    def get_latest_status(self):
        if self.status_packets:
            return self.status_packets[-1]
        else:
            return None

    def get_latest_lap_data(self):
        if self.lap_data_packets:
            return self.lap_data_packets[-1]
        else:
            return None

    def get_latest_car_damage(self):
        if self.car_damage_packets:
            return self.car_damage_packets[-1]
        else:
            return None