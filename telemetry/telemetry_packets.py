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