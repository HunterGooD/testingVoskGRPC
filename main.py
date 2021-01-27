import json
from vosk import Model, KaldiRecognizer
import os
import pyaudio

def getValue(js):
    res = json.loads(js)
    if "result" in res.keys():
        return res["result"]
    elif "partial" in res.keys():
        return res["partial"]
    return ""

if not os.path.exists("model/ru"):
    print ("Please download the model from https://alphacephei.com/vosk/models and unpack as 'model' in the current folder.")
    exit (1)

    
model = Model("model/ru")
recRu = KaldiRecognizer(model, 16000)

model = Model("model/en")
recEn = KaldiRecognizer(model, 16000)

p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8000)
stream.start_stream()

while True:
    data = stream.read(4000)
    if len(data) == 0:
        break
    text = ""
    resText = ""
    if recRu.AcceptWaveform(data):
        text = recRu.Result()
    else:
        text = recRu.PartialResult()
    # print(text)
    valRus = getValue(text)

    if recEn.AcceptWaveform(data):
        text = recEn.Result()
    else:
        text = recEn.PartialResult()
    valEn = getValue(text)
    
    if valEn:
        resText = valEn
    elif valRus:
        resText = valRus
    else:
        resText = ""
        
    # print(text)

print(recRu.FinalResult())