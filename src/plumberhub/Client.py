import requests
import websockets
import asyncio
import threading
from .Store import SampleStore
from .plumberhub_pb2 import Sample

def noop():
    pass

class PlumberHubClient:
    store = SampleStore()

    def __init__(
        self,
        hostname, port, client_id,
        onsample=noop, onerror=noop, onclose=noop
    ):
        host = hostname + ':' + str(port)

        self._base_url = 'http://' + host + '/api/sdk/client/' + client_id
        self.onsample = onsample
        self.onerror = onerror
        self.onclose = onclose

        # Fetching ticket
        response = requests.post(self._base_url + '/session/ticket')
        credential = response.json()['credential']

        # Establishing Data Sample Channel - websocket
        def listen():
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            ws_url = 'ws://' + host + '/client/' + client_id + '/session?credential=' + credential

            async def sample_handler():
                async with websockets.connect(uri=ws_url) as ws:
                    while True:
                        sample = Sample()
                        sample.MergeFromString(await ws.recv())
                        self.onsample(sample)

            loop.run_until_complete(sample_handler())
            onclose()

        listening_thread = threading.Thread(target=listen, args=())
        listening_thread.start()

    def _state(self):
        return self._base_url + '/device/state/'

    def get_device(self):
        response = requests.get(self._base_url + '/device')

        if response.status_code == 200:
            return response.json()

    def get(self, key):
        response = requests.get(self._state() + key)

        if response.status_code == 200:
            return response.json()['value']

    def set(self, key, value):
        response = requests.put(self._state() + key, {'value': value})

        if response.status_code == 200:
            return response.json()['value']
