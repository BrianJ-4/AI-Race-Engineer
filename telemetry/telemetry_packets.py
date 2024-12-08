import struct

class PacketFactory:
    PACKET_ID_MAP = {
        2: 'LapDataPacket',
        6: 'CarTelemetryPacket',
        7: 'CarStatusPacket',
        10: 'CarDamageDataPacket',
    }

    @staticmethod
    def create_packet(header, data):
        packet_id = header.packet_id
        if packet_id == 2:
            return LapDataPacket(data)
        if packet_id == 6:
            return CarTelemetryPacket(data)
        elif packet_id == 7:
            return CarStatusPacket(data)
        elif packet_id == 10:
            return CarDamageDataPacket(data)
        else:
            return None

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
    
class CarStatusData:
    def __init__(self, data, offset):
        self.unpack(data, offset)

    def unpack(self, data, offset):
        status_format = '<5B3f2H2BH3BbfB3fB'
        size = struct.calcsize(status_format)
        unpacked_data = struct.unpack_from(status_format, data, offset)
        (
            self.traction_control,
            self.anti_lock_brakes,
            self.fuel_mix,
            self.front_brake_bias,
            self.pit_limiter_status,
            self.fuel_in_tank,
            self.fuel_capacity,
            self.fuel_remaining_laps,
            self.max_rpm,
            self.idle_rpm,
            self.max_gears,
            self.drs_allowed,
            self.drs_activation_distance,
            self.actual_tyre_compound,
            self.visual_tyre_compound,
            self.tyres_age_laps,
            self.vehicle_fia_flags,
            self.ers_store_energy,
            self.ers_deploy_mode,
            self.ers_harvested_this_lap_mguk,
            self.ers_harvested_this_lap_mguh,
            self.ers_deployed_this_lap,
            self.network_paused,
        ) = unpacked_data
        self.size = size

    def get_size(self):
        return self.size

class LapData:
    def __init__(self, data, offset):
        self.unpack(data, offset)

    def unpack(self, data, offset):
        lap_data_format = '<IIHHfff14B2HB'
        size = struct.calcsize(lap_data_format)
        unpacked_data = struct.unpack_from(lap_data_format, data, offset)
        (
            self.last_lap_time_in_ms,
            self.current_lap_time_in_ms,
            self.sector1_time_in_ms,
            self.sector2_time_in_ms,
            self.lap_distance,
            self.total_distance,
            self.safety_car_delta,
            self.car_position,
            self.current_lap_num,
            self.pit_status,
            self.num_pit_stops,
            self.sector,
            self.current_lap_invalid,
            self.penalties,
            self.warnings,
            self.num_unserved_drive_through_pens,
            self.num_unserved_stop_go_pens,
            self.grid_position,
            self.driver_status,
            self.result_status,
            self.pit_lane_timer_active,
            self.pit_lane_time_in_lane_in_ms,
            self.pit_stop_timer_in_ms,
            self.pit_stop_should_serve_pen,
        ) = unpacked_data
        self.size = size

class CarTelemetryPacket:
    def __init__(self, data):
        self.header = PacketHeader(data)
        self.car_telemetry_data = []
        self.unpack(data)

    def unpack(self, data):
        offset = self.header.get_size()
        num_cars = 22
        for _ in range(num_cars):
            telemetry_data = CarTelemetryData(data, offset)
            self.car_telemetry_data.append(telemetry_data)
            offset += telemetry_data.get_size()


class CarStatusPacket:
    def __init__(self, data):
        self.header = PacketHeader(data)
        self.car_status_data = []
        self.unpack(data)

    def unpack(self, data):
        offset = self.header.get_size()
        num_cars = 22
        for _ in range(num_cars):
            status_data = CarStatusData(data, offset)
            self.car_status_data.append(status_data)
            offset += status_data.get_size()

class LapDataPacket:
    def __init__(self, data):
        self.header = PacketHeader(data)
        self.lap_data = []
        self.unpack(data)

    def unpack(self, data):
        offset = self.header.get_size()
        num_cars = 22
        for _ in range(num_cars):
            lap = LapData(data, offset)
            self.lap_data.append(lap)
            offset += lap.get_size()
        
        time_trial_format = '<BB'
        unpacked_data = struct.unpack_from(time_trial_format, data, offset)
        self.time_trial_pb_car_idx, self.time_trial_rival_car_idx = unpacked_data
        self.size = offset + struct.calcsize(time_trial_format) - self.header.get_size()
    
class CarDamageDataPacket:
    def __init__(self, data):
        self.header = PacketHeader(data)
        self.car_damage_data = []
        self.unpack(data)

    def unpack(self, data):
        offset = self.header.get_size()
        num_cars = 22

        for _ in range(num_cars):
            damage_data = CarDamageData(data, offset)
            self.car_damage_data.append(damage_data)
            offset += damage_data.get_size()

class CarDamageData:
    def __init__(self, data, offset):
        self.unpack(data, offset)

    def unpack(self, data, offset):
        car_damage_format = '<4f4B4B18B'
        size = struct.calcsize(car_damage_format)
        unpacked_data = struct.unpack_from(car_damage_format, data, offset)

        (
            self.tyres_wear_fl, self.tyres_wear_fr, self.tyres_wear_rl, self.tyres_wear_rr,
            td0, td1, td2, td3,
            bd0, bd1, bd2, bd3,
            self.front_left_wing_damage,
            self.front_right_wing_damage,
            self.rear_wing_damage,
            self.floor_damage,
            self.diffuser_damage,
            self.sidepod_damage,
            self.drs_fault,
            self.ers_fault,
            self.gear_box_damage,
            self.engine_damage,
            self.engine_mguh_wear,
            self.engine_es_wear,
            self.engine_ce_wear,
            self.engine_ice_wear,
            self.engine_mguk_wear,
            self.engine_tc_wear,
            self.engine_blown,
            self.engine_seized
        ) = unpacked_data

        # Store tyres and brakes in arrays
        self.tyres_wear = [self.tyres_wear_fl, self.tyres_wear_fr, self.tyres_wear_rl, self.tyres_wear_rr]
        self.tyres_damage = [td0, td1, td2, td3]
        self.brakes_damage = [bd0, bd1, bd2, bd3]

        self.size = size
        
    def get_size(self):
        return self.size