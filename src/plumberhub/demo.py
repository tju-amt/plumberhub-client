import requests
import websockets
import asyncio
import threading
from plumberhub_pb2 import Sample
from plumberhub_pb2 import Event

hostname = '127.0.0.1'
port = 8080
client_id = 'b28572b091a4ac71cf4f02e9df9b674b405dc6c5724be9985a00596e0b9375b5'
host = hostname + ':' + str(port)
base_url = 'http://' + host + '/api/sdk/client/' + client_id
running = True




def listen1(loop):
    dataresponse = requests.post(base_url + '/session/data/ticket')
    datacreeegdential = dataresponse.json()['credential']
    ws_url = 'ws://' + host + '/client/' + client_id + '/session/data?credential=' + datacreeegdential
    
    asyncio.set_event_loop(loop)

    async def sample_handler():
        async with websockets.connect(uri=ws_url) as ws:

            while running:
                sample = Sample()
                sample.MergeFromString(await ws.recv())
                print('1')

    loop.run_until_complete(sample_handler())    


def listen2(loop):
    eventresponse = requests.post(base_url + '/session/event/ticket')
    eventcredential = eventresponse.json()['credential']
    ws_url = 'ws://' + host + '/client/' + client_id + '/session/event?credential=' + eventcredential
    
    asyncio.set_event_loop(loop)

    async def event_handler():
        async with websockets.connect(uri=ws_url) as ws:

            while running:
                event = Event()
                await ws.recv()
                print('2')

    loop.run_until_complete(event_handler())    

thread_loop1 = asyncio.new_event_loop() 
thread_loop2 = asyncio.new_event_loop() 

listening_datathread1 = threading.Thread(target=listen1, args=(thread_loop1,))
listening_datathread1.start()

listening_eventthread2 = threading.Thread(target=listen2, args=(thread_loop2,))
listening_eventthread2.start()

