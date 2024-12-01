from vosk import Model, KaldiRecognizer
from utils.intent_ner_integration import process_input
import sounddevice as sd
import queue
import sys
import json

#Uses default microphone of the system
device_info = sd.query_devices(sd.default.device[0], 'input')
samplerate = int(device_info['default_samplerate'])
print("Default Microphone Device: Description {}".format(device_info))

q = queue.Queue()

def recordCallback(indata, frames, time, status):
    if status:
        print(status, file=sys.stderr)
    q.put(bytes(indata))

def startRecord():
    print("Model and recognizer is building. This will take a few minutes.")
    model = Model(r"SR/model")
    recognizer = KaldiRecognizer(model, samplerate)
    recognizer.SetWords(False)

    print("Begin recording. To finish recording, Say "exit" ")
    try:
        with sd.RawInputStream(dtype='int16',
                            channels=1,
                            callback=recordCallback):
            while True:
                data = q.get()        
                if recognizer.AcceptWaveform(data):
                    rec = recognizer.Result()
                    resultDict = json.loads(rec)
                    if not resultDict.get("text", "") == "":     
                        if resultDict['text'] == "exit":
                            print("Exiting system.")
                            break

                        action_data = process_input(resultDict['text'])
                        #Remove these prints
                        print(resultDict['text'])
                        print(action_data)
                    else:
                        print("No Input Recorded")

    except KeyboardInterrupt:
        print('Finished Recording')
    except Exception as e:
        print(str(e))
