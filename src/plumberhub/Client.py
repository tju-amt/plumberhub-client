import requests
import websockets
import asyncio
import threading
from .PlumberHub_pb2 import Sample
from .PlumberHub_pb2 import Event

def noop():
    pass

class PlumberHubClient:

    def __init__(
        self,
        hostname, port, client_id,
        onready = noop,
        onsample=noop, onevent = noop, 
        onerror=noop, onclose=noop
    ):
        host = hostname + ':' + str(port)

        self._base_url = 'http://' + host + '/api/sdk/client/' + client_id
        self._running = True

        self.onsample = onsample
        self.onevent = onevent
        self.onerror = onerror
        self.onclose = onclose
        self.onready = onready

        # Fetching ticket
        # Establishing Data / Event Channel - websocket
        def listen(channel):
            response = requests.post(self._base_url + '/session/'+channel+'/ticket')
            credential = response.json()['credential']

            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            ws_url = 'ws://' + host + '/client/' + client_id + '/session/'+channel+'?credential=' + credential
            self._loop = loop

            if(channel == 'data'):
                async def sample_handler():
                    async with websockets.connect(uri=ws_url) as ws:
                        threading.Thread(target=self.onready, args=()).start()

                        while self._running:
                            sample = Sample()
                            sample.MergeFromString(await ws.recv())
                            self.onsample(sample)

                loop.run_until_complete(sample_handler())
                onclose()

            elif(channel == 'event'):
                async def event_handler():
                    async with websockets.connect(uri=ws_url) as ws:
                        threading.Thread(target=self.onready, args=()).start()

                        while self._running:
                            event = Event()
                            event.MergeFromString(await ws.recv())
                            self.onevent(event)

                loop.run_until_complete(event_handler())
                onclose()                

        listening_datathread = threading.Thread(target=listen('data'), args=())
        listening_datathread.start()

        listening_eventthread = threading.Thread(target=listen('event'), args=())
        listening_eventthread.start()


    def close(self):
        self._running = False

    def is_master(self):
        response = requests.get(self._base_url + '/profile')

        if response.status_code == 200:
            return response.json()['isMaster']

    def get_device(self):
        response = requests.get(self._base_url + '/device')

        if response.status_code == 200:
            return response.json()

    # Low-level to getting/setting device state.

    def _state(self):
        return self._base_url + '/device/state/'

    def get(self, key):
        response = requests.get(self._state() + key)

        if response.status_code == 200:
            return response.json()['value']

    def set(self, key, value):
        response = requests.put(self._state() + key, {'value': value})

        if response.status_code == 200:
            return response.json()['value']

    # Set sampling on/off

    def _busy(self):
        return self._base_url + '/device/busy'

    def start(self):
        response = requests.put(self._busy(), json = {'value': True})

        if response.status_code == 200:
            return response.json()['value']

    def stop(self):
        response = requests.put(self._busy(), json = {'value': False})

        if response.status_code == 200:
            return response.json()['value']

    # Sampling rate getter/setter

    def _sampling_rate(self):
        return self._base_url + '/device/sampling-rate'

    def get_sampling_rate(self):
        response = requests.get(self._sampling_rate())

        if response.status_code == 200:
            return response.json()['value']

    def set_sampling_rate(self, value):
        response = requests.put(self._sampling_rate(), {'value': value})

        if response.status_code == 200:
            return response.json()['value']

    # Gain getter/setter

    def _gain(self):
        return self._base_url + '/device/gain'

    def get_gain(self):
        response = requests.get(self._gain())

        if response.status_code == 200:
            return response.json()['value']

    def set_gain(self, value):
        response = requests.put(self._gain(), {'value': value})

        if response.status_code == 200:
            return response.json()['value']
