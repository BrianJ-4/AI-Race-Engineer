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
    #TODO Fetch data based on action_data

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