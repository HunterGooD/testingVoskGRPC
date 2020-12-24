from concurrent import futures
import time
import math
import threading
import os

import grpc
from vosk import Model, KaldiRecognizer

import api_pb2_grpc as api
import api_pb2 as api_model


class GrpcServer(api.VoiceToTextServicer):
    def __init__(self, *args, **kwargs):
        model = Model("model")
        self.rec = KaldiRecognizer(model, 16000)

    def GetText(self, request, ctx):
        text = ""
        start = time.time()
        
        if len(request.stream) == 0:
            return api_model.StreamResponse(message="", session_hash=request.session_hash)

        if self.rec.AcceptWaveform(request.stream):
            text = self.rec.Result()
        else:
            text = self.rec.PartialResult()

        end = time.time()
        print(f"Time: {end-start}") # это просто так
        return api_model.StreamResponse(message=text, session_hash=request.session_hash)


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    api.add_VoiceToTextServicer_to_server(GrpcServer(), server)
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
