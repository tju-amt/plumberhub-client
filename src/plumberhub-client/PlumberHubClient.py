import requests
import websockets
import asyncio
import threading
from .plumberhub_pb2 import Sample


def noop():
    pass


class PlumberHubClient:

    def __init__(
            self, hostname, port, clientId,
            onsample=noop, onerror=noop, onclose=noop
    ):
        host = hostname + ':' + str(port)
        baseURL = 'http://' + host + '/api/sdk/client/' + clientId

        self.__baseURL = baseURL
        self.onsample = onsample
        self.onerror = onerror
        self.onclose = onclose

        # Fetching ticket
        response = requests.post(self.__baseURL + '/session/ticket')
        credential = response.json()['credential']

        # Establishing Data Sample Channel - websocket
        def listen():
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            wsURL = 'ws://' + host + '/client/' + clientId + '/session?credential=' + credential

            async def sampleHandler():
                async with websockets.connect(uri=wsURL) as ws:
                    while (True):
                        sample = Sample()
                        sample.MergeFromString(await ws.recv())
                        onsample(sample)

            loop.run_until_complete(sampleHandler())
            onclose()

        listeningThread = threading.Thread(target=listen, args=())
        listeningThread.start()

    def __state(self):
        return self.__baseURL + '/device/state/'

    def get_device(self):
        response = requests.get(self.__baseURL + '/device')

        if (response.status_code == 200):
            return response.json()

    def get(self, key):
        response = requests.get(self.__state() + key)

        if (response.status_code == 200):
            return response.json()['value']

    def set(self, key, value):
        response = requests.put(self.__state() + key, {'value': value})

        if (response.status_code == 200):
            return response.json()['value']
