from threading import Thread
from telemetry.telemetry_listener import TelemetryListener
from telemetry.telemetry_data_store import TelemetryDataStore
from utils.intent_ner_integration import process_input
from vosk import Model, KaldiRecognizer
import sounddevice as sd
import queue
import sys
import json
import time
import os

voice_input_queue = queue.Queue()

# Function to handle telemetry listening
def telemetry_listener(data_store):
    listener = TelemetryListener()

    try:
        print("Telemetry listener started")
        while True:
            packet = listener.receive_packet()
            if packet:
                data_store.add_packet(packet)
            time.sleep(0.01)
    except KeyboardInterrupt:
        print("Telemetry listener stopped")

# Function to handle processing of recognized voice commands
def process_voice_command(data_store, voice_command):
    action_data = process_input(voice_command)
    print(f"Voice Command Action Data: {action_data}")

    if action_data["INTENT"] in ["ask_damage", "ask_temperature"]:
        getDamageOrTemperatureData(data_store, action_data)
    else:
        getTelemetryData(data_store, action_data["INTENT"])

def getDamageOrTemperatureData(data_store, action_data):
    position_mapping = {
        ('front', 'left'): 2,
        ('front', 'right'): 3,
        ('rear', 'left'): 0,
        ('rear', 'right'): 1,
        ('rear', ''): 4,
    }

    direction = action_data.get('DIRECTION', '').lower()
    side = action_data.get('SIDE', '').lower()

    position = position_mapping.get((direction, side), None)
    part = action_data["PART"]

    if part == "brake":        
        if action_data["INTENT"] == "ask_temperature":
            latest_telemetry = data_store.get_latest_telemetry()
            car_data = latest_telemetry.car_telemetry_data[19]
            brake_temp = car_data.brakes_temperature[position]
            print(brake_temp)
        elif action_data["INTENT"] == "ask_damage":
            latest_damage = data_store.get_latest_car_damage()
            player_damage_data = latest_damage.car_damage_data[19]
            brake_damage = player_damage_data.brakes_damage[position]
            print(brake_damage)
    elif part == "tyre" or part == "tire":
        if action_data["INTENT"] == "ask_temperature":
            latest_telemetry = data_store.get_latest_telemetry()
            car_data = latest_telemetry.car_telemetry_data[19]
            tire_temperature = car_data.tyres_surface_temperature[position]
            print(tire_temperature)
        elif action_data["INTENT"] == "ask_damage":
            latest_damage = data_store.get_latest_car_damage()
            player_damage_data = latest_damage.car_damage_data[19]
            tire_damage = player_damage_data.tyres_wear[position]
            print(tire_damage)
    elif part == "wing":
        if action_data["INTENT"] == "ask_damage":
            latest_damage = data_store.get_latest_car_damage()
            player_damage_data = latest_damage.car_damage_data[19]
            if position == 2:
                wing_damage = player_damage_data.front_left_wing_damage
            elif position == 3:
                wing_damage = player_damage_data.front_right_wing_damage
            elif position == 4:
                wing_damage = player_damage_data.rear_wing_damage
            print(wing_damage)

def getTelemetryData(data_store, intent):
    telemetry_actions = {
        "ask_last_lap_time": lambda car_data: print(f"Your last lap was a : {car_data.last_lap_time_in_ms / 1000}"),
        "ask_current_position": lambda car_data: print(f"You're currently in {car_data.car_position}"),
        "ask_current_lap": lambda car_data: print(f"It is {car_data.current_lap_num}"),
        "ask_start_position": lambda car_data: print(f"You started in {car_data.grid_position}"),
        "ask_remaining_fuel": lambda car_data: print(f"We have {car_data.fuel_remaining_laps} laps of fuel left"),
        "ask_tire_compound": lambda car_data: print(f"You are using {car_data.visual_tyre_compound}"),
        "ask_tire_age": lambda car_data: print(f"These tires are {car_data.tyres_age_laps} laps old"),
    }

    if intent in ["ask_last_lap_time", "ask_current_position", "ask_current_lap", "ask_start_position"]:
        latest_lap_data = data_store.get_latest_lap_data()
        car_data = latest_lap_data.lap_data[19]
    elif intent in ["ask_remaining_fuel", "ask_tire_compound", "ask_tire_age"]:
        latest_status = data_store.get_latest_status()
        car_data = latest_status.car_status_data[19]

    telemetry_actions[intent](car_data)

# Function to handle voice input
def voice_listener(data_store):
    device_info = sd.query_devices(sd.default.device[0], 'input')
    samplerate = int(device_info['default_samplerate'])
    print(f"Default Microphone Device: {device_info}")

    model_path = os.path.abspath("SR/model")
    model = Model(model_path)
    recognizer = KaldiRecognizer(model, samplerate)
    recognizer.SetWords(False)

    print("Voice listener started. Say 'exit' to quit.")

    def record_callback(indata, frames, time, status):
        if status:
            print(status, file=sys.stderr)
        voice_input_queue.put(bytes(indata))

    try:
        with sd.RawInputStream(dtype = 'int16', channels = 1, samplerate = samplerate, callback = record_callback):
            while True:
                data = voice_input_queue.get()
                if recognizer.AcceptWaveform(data):
                    rec = recognizer.Result()
                    result_dict = json.loads(rec)
                    if result_dict.get("text", ""):
                        print(f"Recognized Voice Command: {result_dict['text']}") # Need to delete
                        if result_dict['text'] == "exit":
                            print("Exiting system")
                            break
                        if result_dict['text'] == "the": #Deals with issue of hearing "the" when quiet
                            continue
                        process_voice_command(data_store, result_dict['text'])
    except Exception as e:
        print(f"Voice listener error: {e}")

def main():
    # Create shared TelemetryDataStore
    data_store = TelemetryDataStore()

    # Start telemetry listener thread
    telemetry_thread = Thread(target = telemetry_listener, args = (data_store,))
    telemetry_thread.daemon = True
    telemetry_thread.start()

    # Start voice listener
    voice_listener(data_store)

if __name__ == "__main__":
    main()