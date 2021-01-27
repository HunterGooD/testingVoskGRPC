import os
import time

import grpc
import pyaudio

import api_pb2_grpc as api
import api_pb2 as api_model


def run():
    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8000)
    stream.start_stream()
    with grpc.insecure_channel("localhost:9020") as chanel:
        stub = api.VoiceRecognizerStub(chanel)
        while True:
            try:
                data = stream.read(4000)
                req = api_model.GetTextRequest()
                req.stream = data
                req.bitrate = 0
                req.sampleRate = 16000
                response = stub.GetText(req)
                if response.message != "":
                    print(response.message)
            except KeyboardInterrupt:
                print("Stoped")
                chanel.unsubscribe(close)
                exit(0)


def close(chanel):
    chanel.close()


if __name__ == "__main__":
    run()
