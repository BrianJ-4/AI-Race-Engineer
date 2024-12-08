import struct

class PacketHeader:
    def __init__(self, data):
        self.unpack(data)

    def unpack(self, data):
        header_format = '<HBBBBQfI2B'  # Little-endian format
        unpacked_data = struct.unpack_from(header_format, data)
        (
            self.packet_format,
            self.game_major_version,
            self.game_minor_version,
            self.packet_version,
            self.packet_id,
            self.session_uid,
            self.session_time,
            self.frame_identifier,
            self.player_car_index,
            self.secondary_player_car_index,
        ) = unpacked_data

    def get_size(self):
        return struct.calcsize('<HBBBBQfI2B')
    
class CarTelemetryData:
    def __init__(self, data, offset):
        self.unpack(data, offset)

    def unpack(self, data, offset):
        telemetry_format = '<HfffBbHBBH4H4B4BH4f4B'
        size = struct.calcsize(telemetry_format)
        unpacked_data = struct.unpack_from(telemetry_format, data, offset)
        (
            self.speed,
            self.throttle,
            self.steer,
            self.brake,
            self.clutch,
            self.gear,
            self.engine_rpm,
            self.drs,
            self.rev_lights_percent,
            self.rev_lights_bit_value,
        ) = unpacked_data[:10]

        self.brakes_temperature = list(unpacked_data[10:14])       
        self.tyres_surface_temperature = list(unpacked_data[14:18])
        self.tyres_inner_temperature = list(unpacked_data[18:22])  
        self.engine_temperature = unpacked_data[22]               
        self.tyres_pressure = list(unpacked_data[23:27])           
        self.surface_type = list(unpacked_data[27:31])  

        self.size = size

    def get_size(self):
        return self.size