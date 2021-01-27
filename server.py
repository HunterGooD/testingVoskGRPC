from concurrent import futures
import time
import math
import threading
import os
import json

import grpc
from vosk import Model, KaldiRecognizer

import api_pb2_grpc as api
import api_pb2 as api_model


class GrpcServer(api.VoiceRecognizerServicer):
    def __init__(self, *args, **kwargs):
        model = Model("model/ru")
        self.recRu = KaldiRecognizer(model, 16000)
        model = Model("model/en")
        self.recEn = KaldiRecognizer(model, 16000)

    def GetText(self, request, ctx):
        
        if len(request.stream) == 0:
            return api_model.GetTextResponse(message="")

        if request.sampleRate != 16000:
            pass
        
        valRus = self.RecognizerRus(request.stream)
        valEn = self.RecognizerEn(request.stream)

        text = valRus if valRus != "" else valEn if valEn != "" else ""

        return api_model.GetTextResponse(message=text)

    def RecognizerRus(self, stream):
        if self.recRu.AcceptWaveform(stream):
            text = self.recRu.Result()
        else:
            text = self.recRu.PartialResult()
        return self.getValue(text)

    def RecognizerEn(self, stream):
        if self.recEn.AcceptWaveform(stream):
            text = self.recEn.Result()
        else:
            text = self.recEn.PartialResult()
        return self.getValue(text)

    def getValue(self, js):
        res = json.loads(js)
        if "result" in res.keys():
            return json.dumps(res["result"])
        elif "partial" in res.keys():
            return res["partial"]
        return ""

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    api.add_VoiceRecognizerServicer_to_server(GrpcServer(), server)
    server.add_insecure_port("[::]:9020")
    server.start()
    try:
        while True:
            print(f"server thread: {threading.active_count()}")
            time.sleep(5)
    except KeyboardInterrupt:
        print("Server stoped")
        server.stop(0)

if __name__ == '__main__':
    serve()
